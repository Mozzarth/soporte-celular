"""Reconstruye el soporte completo en la ventana de SolidCraft abierta con `solidcraft --control 7878`.

Corre paso a paso (se ve construirse), elige las aristas de cada redondeo sobre el modelo de ese
momento, guarda soporte.solidcraft y exporta soporte.json, el script que lo rehace sin la ventana.

  python3 todo.py
"""
import json, math, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import live, boca, punta

AQUI = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(AQUI, 'gen.py')).read().split("n = int(sys.argv[1])")[0]
G = {}
exec(src, G)
AI, PROF, ESP, HF, ALTO_B, AE = G['AI'], G['PROF'], G['ESP'], G['HF'], G['ALTO_B'], G['AE']


def txt(r):
    return ''.join(c['text'] for c in r['result']['content'] if c.get('type') == 'text')


def esperar():
    time.sleep(3)
    for _ in range(180):
        if '"running": []' in txt(live.llamar('running')):
            return
        time.sleep(10)


def ej(command, params):
    r = live.llamar('execute', {'command': command, 'params': params, 'verbose': False})
    o = txt(r)
    if 'still running' in o:
        esperar()
    elif r['result'].get('isError'):
        sys.exit(f'ERROR en {command}: {o[:300]}')
    return o


def correr(cmds):
    for c in cmds:
        ej(c['command'], c['params'])


def aristas():
    return json.loads(txt(live.llamar('execute', {'command': 'model.edges', 'params': {'body': 'soporte'}})))['edges']


def plana(e, k, v, tol=1e-3):
    return abs(e['start'][k] - v) < tol and abs(e['end'][k] - v) < tol


def cerca_punta(m):
    return abs(abs(m[0]) - HF / 2) < 1.6 and m[1] < -9


t0 = time.time()
def paso(nombre):
    print(f'{time.time() - t0:6.0f} s  {nombre}', flush=True)


live.llamar('new_design', {'name': 'soporte'})

paso('placa, bolsillo, aberturas y piso hueco')
G['stage'](3)
G['fillets_verticales']()
correr(G['C'])
ej('solid.fillet', {'edges': G['concavas_piso'](aristas()), 'radius': 2})

paso('nombre calado: la O se corta en dos mitades y el puente queda sin cortar')
correr([
    {'command': 'sketch.create', 'params': {'plane': 'XZ', 'flip': True, 'name': 'nombre'}},
    {'command': 'sketch.text', 'params': {'text': 'MOISES', 'at': [0, 60.5], 'height': 9,
                                          'font': 'JetBrainsMono Nerd Font', 'bold': True, 'align': 'center'}},
    {'command': 'sketch.rectangle.two_point', 'params': {'p0': [-12.1, 59.5], 'p1': [-10.1, 70.5]}},
    {'command': 'sketch.finish', 'params': {}},
    # 0 M · 1 y 6 mitades de la O · 10-13 I S E S (el centro y los puentes de la O no se cortan)
    {'command': 'solid.extrude', 'params': {'profiles': [0, 1, 6, 10, 11, 12, 13], 'through_all': True,
                                            'direction': 'symmetric', 'operation': 'cut'}},
])

paso('puntos en degradado')
puntos = [{'command': 'sketch.create', 'params': {'plane': 'XZ', 'flip': True, 'name': 'puntos'}}]
for iz in range(7):
    for ix in range(-6, 7):
        x = ix * 6.6 + (iz % 2) * 3.3
        z = 9 + 3 + iz * 6.6
        r = 0.8 + 2.1 * (1 - iz / 6)
        if abs(x) + r <= 36 and z + r <= 55:
            puntos.append({'command': 'sketch.circle.center', 'params': {'center': [round(x, 3), round(z, 3)], 'radius': round(r, 3)}})
puntos += [{'command': 'sketch.finish', 'params': {}},
           {'command': 'solid.extrude', 'params': {'profiles': 'all', 'distance': 6, 'direction': 'symmetric', 'operation': 'cut'}}]
correr(puntos)

paso('rebajes de 0.5 mm para la cinta, en la espalda')
xp, xb = 36, AE - 2
rebajes = [{'command': 'sketch.create', 'params': {'plane': 'XZ', 'flip': True, 'offset': ESP, 'name': 'rebajes'}}]
for p0, p1 in [([-24, 72], [24, 77]), ([-xp, 2], [xp, 8]), ([xp + 1.5, 11], [xb, 60]), ([-xb, 11], [-xp - 1.5, 60])]:
    rebajes.append({'command': 'sketch.rectangle.rounded', 'params': {'p0': p0, 'p1': p1, 'radius': 1.5}})
rebajes += [{'command': 'sketch.finish', 'params': {}},
            {'command': 'solid.extrude', 'params': {'profiles': 'all', 'distance': 0.5, 'direction': 'positive', 'operation': 'cut'}}]
correr(rebajes)

paso('entrada redondeada de los puntos')
E = aristas()
ej('solid.fillet', {'edges': [e['mid'] for e in E if plana(e, 1, 0) and abs(e['mid'][0]) < 37 and 8 < e['mid'][2] < 58],
                    'radius': 0.35})

paso('bordes: contorno de la placa, reborde del piso y base')
E = aristas()
placa = [e['mid'] for e in E if plana(e, 1, 0) and e['mid'][2] > ALTO_B
         and not (abs(e['mid'][0]) < 23 and 59 < e['mid'][2] < 71) and not (abs(e['mid'][0]) < 37 and e['mid'][2] < 56)]
ej('solid.fillet', {'edges': placa, 'radius': 0.9})
E = aristas()
reborde = [e['mid'] for e in E if plana(e, 2, 2) and abs(abs(e['mid'][0]) - AI / 2) > 3 and e['mid'][1] < -3
           and (abs(e['mid'][0]) <= HF / 2 or e['mid'][1] > -(PROF - 3)) and not cerca_punta(e['mid'])]
ej('solid.fillet', {'edges': reborde, 'radius': 0.9})
E = aristas()
base = [e['mid'] for e in E if plana(e, 2, 0) and e['mid'][1] < ESP - 0.01 and not cerca_punta(e['mid'])]
ej('solid.fillet', {'edges': base, 'radius': 0.45})

paso('boca en embudo')
correr(boca.comandos() + boca.unir() + boca.abertura())
E = aristas()
z = boca.Z0 + boca.ALTO
canto = [e['mid'] for e in E if plana(e, 2, z) and not (e['start'][1] > ESP - 0.1 and e['end'][1] > ESP - 0.1)
         and e['length'] > 2 and abs(e['mid'][0]) > 30]
ej('solid.fillet', {'edges': canto, 'radius': 0.6, 'body': 'soporte'})
correr(punta.comandos())
ej('browser.visibility', {'folder': 'sketches', 'visible': False})

paso('guardar')
live.llamar('save', {'path': os.path.join(AQUI, 'soporte.solidcraft')})
ej('timeline.export_script', {'path': os.path.join(AQUI, 'soporte.json')})
d = json.loads(txt(live.llamar('inspect_design', {'sketches': False})))
print('errores:', [(x['name'], x['error']) for x in d['timeline'] if x.get('error')] or 'ninguno')
print('cuerpos:', [(b['name'], round(b.get('volume_mm3', 0)), [round(v, 1) for v in b['bbox']['min']],
                    [round(v, 1) for v in b['bbox']['max']]) for b in d['bodies']])
paso('listo')
