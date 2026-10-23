"""Punta del embudo redondeada vista de frente: un corte en arco en la esquina de arriba, a cada lado.

El arco cruza la cara de la punta y el canto con un ángulo leve, en vez de tocarlos tangente: caras
que coinciden o se rozan hacen fallar el corte ("coincident faces") y no corta nada.
"""
import math

PROF = 13                           # profundidad del bolsillo: el corte arranca detrás de la cara interior de la aleta
HF, ZTOP, R = 66.5, 50, 4.5          # abertura frontal, altura de la boca, radio del arco
CRUCE = 0.3                         # cuánto se mete el centro del arco para cruzar en vez de rozar


def comandos():
    C = [{"command": "sketch.create", "params": {"plane": "XZ", "flip": True, "offset": -(PROF - 2), "name": "punta_boca"}}]
    d = math.sqrt(R * R - (R - CRUCE) ** 2)       # dónde corta el círculo la punta y el canto
    for s in (-1, 1):
        x0 = s * HF / 2                            # cara de la punta (borde de la abertura)
        cx, cz = x0 + s * (R - CRUCE), ZTOP - R + CRUCE
        a = [x0, cz + d]                           # cruce con la cara de la punta
        b = [cx - s * d, ZTOP]                     # cruce con el canto
        medio = [cx - s * R * math.cos(math.pi / 4), cz + R * math.sin(math.pi / 4)]
        afuera = x0 - s * 0.5                      # dentro de la abertura, donde no hay material
        C += [
            # la base baja en diagonal hacia la abertura: si queda a la altura del cruce, roza la punta y deja grietas
            {"command": "sketch.line", "params": {"points": [a, [afuera, a[1] - 0.25], [afuera, ZTOP + 1], [b[0], ZTOP + 1], b]}},
            {"command": "sketch.arc.three_point", "params": {"start": b, "end": a, "through": medio}},
        ]
    C += [
        {"command": "sketch.finish", "params": {}},
        # desde y = -(PROF - 2) hacia adelante: toma toda la punta y no toca la placa
        {"command": "solid.extrude", "params": {"profiles": "all", "distance": 8, "direction": "positive",
                                                "operation": "cut", "name": "punta_boca"}},
    ]
    return C
