"""Nombre calado tipo esténcil: cada letra con hueco cerrado (A, D, O, R...) lleva un puente vertical
sin cortar que sostiene su centro. Elige qué perfiles cortar mirando el boceto con solidcraft-cli."""
import json, os, subprocess, sys, tempfile

TEXTO = "ERWIN"
FUENTE = "JetBrainsMono Nerd Font"
ALTO, Z_BASE = 9, 60.5             # altura de las mayúsculas y línea base
PUENTE = 2                         # ancho del puente


def _boceto(extra=()):
    cmds = [{"command": "sketch.create", "params": {"plane": "XZ", "flip": True, "name": "nombre"}},
            {"command": "sketch.text", "params": {"text": TEXTO, "at": [0, Z_BASE], "height": ALTO,
                                                  "font": FUENTE, "bold": True, "align": "center"}}]
    return cmds + list(extra)


def _perfiles(cmds):
    with tempfile.TemporaryDirectory() as d:
        s, r = os.path.join(d, 's.json'), os.path.join(d, 'r.json')
        json.dump({"commands": cmds + [{"command": "sketch.inspect", "params": {}}]}, open(s, 'w'))
        subprocess.run(['solidcraft-cli', 'run', s, '--results', '--json-out', r], capture_output=True, check=True)
        return json.load(open(r))[-1]


def _dentro(p, poli):
    x, y = p
    adentro = False
    for (x1, y1), (x2, y2) in zip(poli, poli[1:] + poli[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            adentro = not adentro
    return adentro


def _area(poli):
    return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(poli, poli[1:] + poli[:1]))) / 2


def comandos():
    # 1. huecos cerrados de las letras: perfiles que son el agujero de otro
    b = _perfiles(_boceto())
    curva = {c['id']: c for c in b['curves']}
    huecos = []
    for p in b['profiles']:
        for h in p['holes']:
            pts = []
            for cid in h:
                a = curva[cid]['start_at']
                if not pts or pts[-1] != a:
                    pts.append(a)
            huecos.append(pts)
    # el puente va solo debajo del hueco: lo sostiene desde abajo (la pieza se imprime de pie) y la
    # parte de arriba de la letra queda entera (la punta de la A, el arco de la D)
    puentes = []
    for h in huecos:
        xs = [x for x, _ in h]
        xc = (min(xs) + max(xs)) / 2
        puentes.append((xc - PUENTE / 2, xc + PUENTE / 2, min(y for _, y in h) + 0.3))
    # 2. el boceto con los puentes: se cortan los trazos, no los huecos ni lo que queda dentro de un puente
    rects = [{"command": "sketch.rectangle.two_point",
              "params": {"p0": [x0, Z_BASE - 1], "p1": [x1, ytop]}} for x0, x1, ytop in puentes]
    b2 = _perfiles(_boceto(rects))
    # sin cortar quedan solo las piezas chicas: el hueco de la letra y lo que cae dentro de un puente
    # (una letra entera puede tener el centro ahí, pero es mucho más grande)
    cortar = []
    for p in b2['profiles']:
        x, y = p['centroid_sketch']
        a = p['area_mm2']
        if any(x0 < x < x1 and y < ytop and a <= (x1 - x0) * (ytop - Z_BASE + 1) + 0.5 for x0, x1, ytop in puentes):
            continue
        if any(_dentro((x, y), h) and a <= _area(h) + 0.5 for h in huecos):
            continue
        cortar.append(p['index'])
    return _boceto(rects) + [
        {"command": "sketch.finish", "params": {}},
        {"command": "solid.extrude", "params": {"profiles": cortar, "through_all": True,
                                                "direction": "symmetric", "operation": "cut", "name": "nombre"}},
    ], len(puentes), len(cortar)


if __name__ == '__main__':
    c, n, k = comandos()
    print(f'{TEXTO}: {n} puentes, {k} perfiles a cortar', file=sys.stderr)
    json.dump({"commands": c}, sys.stdout, indent=1)
