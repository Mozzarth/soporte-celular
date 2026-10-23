import json, sys
AI, PROF, PARED, ESP, ALTO, ALTO_B = 84.5, 13, 2.0, 2.5, 80, 45.5
HF, HP = 66.5, 56                # aberturas: frente y piso
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
    # ranura del piso para el cable (HP de ancho, más angosta que la abertura frontal), abierta al frente y con las esquinas de atrás
    # redondeadas; a los lados el piso queda lleno (sostiene el teléfono) y atrás queda una franja de 3.5 mm
    # al llegar al frente la ranura se abre en curva (radio RF): la esquina del piso queda redonda
    RF = 2
    cmd("sketch.create", plane="XY", offset=-1, name="piso_hueco")
    cmd("sketch.line", points=[[HP/2, -FONDO + RF], [HP/2, -3.5], [-HP/2, -3.5], [-HP/2, -FONDO + RF]])
    for s in (-1, 1):
        c = [s * (HP/2 + RF), -FONDO + RF]
        m = [c[0] - s * RF * 0.7071, c[1] - RF * 0.7071]
        cmd("sketch.arc.three_point", start=[s * HP/2, -FONDO + RF], end=[s * (HP/2 + RF), -FONDO], through=m)
    cmd("sketch.line", points=[[HP/2 + RF, -FONDO], [HP/2 + RF, -FONDO - 1], [-HP/2 - RF, -FONDO - 1], [-HP/2 - RF, -FONDO]])
    cmd("sketch.fillet", points=["l1.end", "l2.end"], radius=4)
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
