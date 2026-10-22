import json, sys
AI, PROF, PARED, ESP, ALTO, ALTO_B = 86, 16, 2.0, 2.5, 80, 45.5
HF, HP = 70, 56                # aberturas: frente y piso
BORDE = 6                      # ancho del reborde del piso junto a las paredes
AE = AI / 2 + PARED            # medio ancho exterior
FONDO = PROF + PARED
C = []
def cmd(c, **p): C.append({"command": c, "params": p})
def stage(n):
    # placa
    cmd("sketch.create", plane="XZ", flip=True, name="placa")
    cmd("sketch.rectangle.two_point", p0=[-AE, 0], p1=[AE, ALTO])
    cmd("sketch.fillet", points=["p3", "p4"], radius=12)
    cmd("sketch.finish")
    cmd("solid.extrude", distance=ESP, direction="negative", body_name="soporte")
    if n < 2: return
    # bolsillo
    cmd("sketch.create", plane="XY", name="bolsillo")
    cmd("sketch.rectangle.two_point", p0=[-AE, -FONDO], p1=[AE, 0])
    cmd("sketch.finish")
    cmd("solid.extrude", distance=ALTO_B, operation="join")
    cmd("sketch.create", plane="XY", offset=PARED, name="hueco")
    cmd("sketch.rectangle.two_point", p0=[-AI/2, -PROF], p1=[AI/2, 0])
    cmd("sketch.finish")
    cmd("solid.extrude", distance=ALTO_B, operation="cut")
    # abertura frontal (solo paredes, sobre el piso)
    cmd("sketch.create", plane="XY", offset=PARED, name="abertura")
    cmd("sketch.rectangle.two_point", p0=[-HF/2, -FONDO - 1], p1=[HF/2, -PROF + 0.5])
    cmd("sketch.finish")
    cmd("solid.extrude", distance=ALTO_B, operation="cut")
    # ranura del piso
    # piso hueco: solo queda un reborde de BORDE mm junto a cada pared y la franja trasera
    xi = AI / 2 - BORDE
    cmd("sketch.create", plane="XY", offset=-1, name="piso_hueco")
    yf = -PROF + BORDE                     # el reborde también sigue por detrás de las aletas
    cmd("sketch.line", closed=True, points=[[-HF/2, -FONDO - 1], [HF/2, -FONDO - 1], [HF/2, yf], [xi, yf],
                                            [xi, -3.5], [-xi, -3.5], [-xi, yf], [-HF/2, yf]])
    cmd("sketch.fillet", points=["l4.end", "l5.end"], radius=4)
    cmd("sketch.fillet", points=["l3.end", "l6.end"], radius=1.5)   # la vuelta del reborde, en curva
    cmd("sketch.finish")
    cmd("solid.extrude", distance=PARED + 2, operation="cut")
def fillets_verticales():
    zm = 26
    cmd("solid.fillet", edges=[[-AI/2, -PROF, zm], [AI/2, -PROF, zm]], radius=5)
    cmd("solid.fillet", edges=[[-AE, -FONDO, zm], [AE, -FONDO, zm]], radius=7)
    cmd("solid.fillet", edges=[[-AI/2, 0, zm], [AI/2, 0, zm]], radius=2)
    # puntas de las aletas
    cmd("solid.fillet", edges=[[s*HF/2, y, zm] for s in (-1, 1) for y in (-FONDO, -PROF)], radius=0.7)
def concavas_piso(E):
    out = []
    for e in E:
        if abs(e['start'][2] - 2) > 1e-6 or abs(e['end'][2] - 2) > 1e-6: continue
        x, y, _ = e['mid']
        # cóncavas: donde el piso se junta con las paredes laterales, la placa o las aletas
        if (abs(abs(x) - AI/2) < 0.1 or y > -0.7 or (y < -14 and abs(x) > AI/2 - 2.5)
                or (abs(y + PROF) < 0.1 and abs(x) > HF/2)
                or (abs(abs(x) - HF/2 - 0.3) < 0.6 and y < -15.3)):
            out.append(e['mid'])
    return out
n = int(sys.argv[1]); extra = sys.argv[2:] 
stage(n)
if n >= 3: fillets_verticales()
for e in extra: C.append(json.loads(e))
json.dump({"commands": C}, sys.stdout, indent=1)
