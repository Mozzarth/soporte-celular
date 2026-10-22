import json, subprocess, sys
S = sys.argv[1] if len(sys.argv) > 1 else '.'
sys.argv = ['gen.py', '3']
src = open(f'{S}/gen.py').read().replace("n = int(sys.argv[1]); extra = sys.argv[2:] \nstage(n)\nif n >= 3: fillets_verticales()\nfor e in extra: C.append(json.loads(e))\njson.dump({\"commands\": C}, sys.stdout, indent=1)\n", "")
ns = {}; exec(src, ns)
cmd, C = ns['cmd'], ns['C']
def correr(extra=None, out=None):
    cmds = C + ([extra] if extra else [])
    json.dump({"commands": cmds}, open(f'{S}/cur.json', 'w'))
    a = ['solidcraft-cli', 'run', f'{S}/cur.json', '--results', '--json-out', f'{S}/cur_r.json']
    if out: a += ['--out', out]
    p = subprocess.run(a, capture_output=True, text=True)
    if p.returncode: print(p.stderr.strip()[-600:]); sys.exit(1)
    return json.load(open(f'{S}/cur_r.json'))
def edges():
    return correr({"command": "model.edges", "params": {"body": "soporte"}})[-1]['edges']
ns['stage'](3); ns['fillets_verticales']()
cmd("solid.fillet", edges=ns['concavas_piso'](edges()), radius=2)
# nombre calado (sin el centro de la O) + puente esténcil
cmd("sketch.create", plane="XZ", flip=True, name="nombre")
cmd("sketch.text", text="MOISES", at=[0, 60.5], height=9, font="JetBrainsMono Nerd Font", bold=True, align="center")
cmd("sketch.finish")
cmd("solid.extrude", profiles=[0, 1, 3, 4, 5, 6], through_all=True, direction="symmetric", operation="cut")
cmd("solid.box", length=2, width=ns['ESP'], height=9.6, corner=[-12.1, 0, 60.2], operation="join", targets=["soporte", "soporte (1)"])
# puntos en degradado
cmd("sketch.create", plane="XZ", flip=True, name="puntos")
for iz in range(7):
    for ix in range(-6, 7):
        x = ix * 6.6 + (iz % 2) * 3.3; z = 9 + 3 + iz * 6.6
        rr = 0.8 + 2.1 * (1 - iz / 6)
        if abs(x) + rr <= 36 and z + rr <= 55:
            cmd("sketch.circle.center", center=[round(x, 3), round(z, 3)], radius=round(rr, 3))
cmd("sketch.finish")
cmd("solid.extrude", profiles="all", distance=6, direction="symmetric", operation="cut")
# rebajes para cinta en la espalda (y = ESP), 0.5 mm
cmd("sketch.create", plane="XZ", flip=True, offset=ns["ESP"], name="rebajes")  # offset va por la normal sin girar (+Y): la espalda
xp = 36; xb = ns['AE'] - 2
for p0, p1 in [([-24, 72], [24, 77]), ([-xp, 2], [xp, 8]), ([xp + 1.5, 11], [xb, 60]), ([-xb, 11], [-xp - 1.5, 60])]:
    cmd("sketch.rectangle.rounded", p0=p0, p1=p1, radius=1.5)
cmd("sketch.finish")
cmd("solid.extrude", profiles="all", distance=0.5, direction="positive", operation="cut")
json.dump({"commands": C}, open(f'{S}/base.json', 'w'))
E = edges()
def en(e, k, v): return abs(e['start'][k] - v) < 1e-4 and abs(e['end'][k] - v) < 1e-4
huecos = [e['mid'] for e in E if en(e, 1, 0) and abs(e['mid'][0]) < 37 and 8 < e['mid'][2] < 58]  # solo puntos
print('aristas de huecos:', len(huecos))
json.dump(huecos, open(f'{S}/huecos.json', 'w'))
import time; t = time.time()
cmd("solid.fillet", edges=huecos, radius=0.35)
r = correr()
print('fillet huecos s', round(time.time() - t, 1))
print([(x['name'], round(x['ms']), x.get('warning')) for x in r if isinstance(x, dict) and 'ms' in x and x['ms'] > 100])
json.dump({"commands": C}, open(f'{S}/modelo.json', 'w'), indent=1)
