"""Punta del embudo redondeada vista de frente: un corte en arco en la esquina superior, a cada lado."""
import math

HF, ZTOP, R = 66, 50, 2.5          # abertura frontal, altura de la boca, radio de la punta


def comandos():
    C = [{"command": "sketch.create", "params": {"plane": "XZ", "flip": True, "offset": -14, "name": "punta_boca"}}]
    for s in (-1, 1):
        x0 = s * HF / 2                       # canto de la abertura
        cx, cz = x0 + s * R, ZTOP - R         # centro del arco
        t = [cx - s * R * math.cos(math.pi / 4), cz + R * math.sin(math.pi / 4)]
        C += [
            {"command": "sketch.line", "params": {"points": [[x0, cz], [x0, ZTOP + 1], [cx, ZTOP + 1], [cx, ZTOP]]}},
            {"command": "sketch.arc.three_point", "params": {"start": [cx, ZTOP], "end": [x0, cz], "through": t}},
        ]
    C += [
        {"command": "sketch.finish", "params": {}},
        # desde y = -14 hacia adelante: solo toca el frente de la boca, no la placa
        {"command": "solid.extrude", "params": {"profiles": "all", "distance": 8, "direction": "positive",
                                                "operation": "cut", "name": "punta_boca"}},
    ]
    return C
