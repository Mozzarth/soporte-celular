"""Boca en forma de embudo sobre las paredes: se abre hacia el frente y los lados, la placa queda recta."""
import json, sys

AI, PROF, PARED, HF = 86, 16, 2.0, 66
Z0, ALTO, ABRE = 45.5, 4.5, 2      # paredes de 45.5 (con 45 exactos SolidCraft falla el filete del piso); la boca termina a 50
ESP = 2.5                          # la boca llega hasta la espalda: queda unida a la placa
R_BORDE = 0.8                      # redondeo del canto de la boca
AE, FONDO = AI / 2 + PARED, PROF + PARED


def contorno(nombre, z, medio_ancho, fondo, radio, atras=0):
    """U abierta hacia la placa (hasta y = atras), con las esquinas del frente redondeadas."""
    return [
        {"command": "sketch.create", "params": {"plane": "XY", "offset": z, "name": nombre}},
        {"command": "sketch.line", "params": {"closed": True, "points": [
            [-medio_ancho, atras], [-medio_ancho, -fondo], [medio_ancho, -fondo], [medio_ancho, atras]]}},
        {"command": "sketch.fillet", "params": {"points": ["l1.end", "l2.end"], "radius": radio}},
        {"command": "sketch.finish", "params": {}},
    ]


def comandos():
    C = []
    # la boca se arma como pieza aparte y después se une al soporte. Abajo arranca 1 mm metida dentro de la
    # pared y 0.3 mm más angosta que ella: así se superponen en volumen y sus caras se cruzan en vez de
    # coincidir, que es lo que el motor no logra unir.
    C += contorno("boca_ext_0", Z0 - 1, AE - 0.3, FONDO - 0.3, 7 - 0.3, atras=ESP - 0.3)
    C += contorno("boca_ext_2", Z0 + ALTO, AE + ABRE, FONDO + ABRE, 7 + ABRE, atras=ESP)
    C.append({"command": "solid.loft", "params": {"sections": [{"sketch": "boca_ext_0"}, {"sketch": "boca_ext_2"}],
                                                   "operation": "new", "name": "boca", "body_name": "boca"}})
    # el hueco: atrás pasa la espalda (solo corta la boca) y arriba sube 1 mm más con la misma pendiente,
    # porque caras al mismo nivel dejan una tapa de grosor cero
    extra = ABRE * (ALTO + 2) / ALTO
    C += contorno("boca_int_0", Z0 - 1, AI / 2, PROF, 5, atras=ESP + 1)
    C += contorno("boca_int_2", Z0 + ALTO + 1, AI / 2 + extra, PROF + extra, 5 + extra, atras=ESP + 1)
    C.append({"command": "solid.loft", "params": {"sections": [{"sketch": "boca_int_0"}, {"sketch": "boca_int_2"}],
                                                   "operation": "cut", "targets": ["boca"], "name": "boca_hueco"}})
    return C


def abertura():
    """La abertura frontal atraviesa la boca (después de unirla, así es una sola unión)."""
    return [
        {"command": "sketch.create", "params": {"plane": "XY", "offset": Z0 - 2, "name": "boca_abertura"}},
        {"command": "sketch.rectangle.two_point", "params": {"p0": [-HF / 2, -FONDO - ABRE - 2], "p1": [HF / 2, -PROF + 0.5]}},
        {"command": "sketch.finish", "params": {}},
        {"command": "solid.extrude", "params": {"distance": ALTO + 3, "operation": "cut", "targets": ["soporte"], "name": "boca_abertura"}},
    ]


def redondeo(E):
    """Aristas del canto de arriba de la boca."""
    z = Z0 + ALTO
    return [e['mid'] for e in E if abs(e['start'][2] - z) < 1e-3 and abs(e['end'][2] - z) < 1e-3
            and not (e['start'][1] > ESP - 0.1 and e['end'][1] > ESP - 0.1)]   # sin la espalda


def unir():
    return [{"command": "solid.combine", "params": {"target": "soporte", "tools": ["boca"], "operation": "join"}}]


if __name__ == '__main__':
    json.dump({"commands": comandos()}, sys.stdout, indent=1)
