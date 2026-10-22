"""Elige las aristas exteriores para el redondeo de 0.9 mm (no la espalda, ni puntos, ni letras)."""
import json, sys
AI, PROF, ESP, HF, BORDE = 86, 16, 2.5, 66, 6

def en(e, k, v, tol=1e-3):
    return abs(e['start'][k] - v) < tol and abs(e['end'][k] - v) < tol

def exteriores(E):
    out = []
    for e in E:
        x, y, z = e['mid']
        if max(e['start'][1], e['end'][1]) > ESP - 1e-3 and min(e['start'][1], e['end'][1]) > ESP - 0.6:
            continue                                   # espalda y rebajes
        if en(e, 2, 50):
            out.append(e['mid'])                      # cantos de arriba de paredes y aletas
        elif en(e, 1, 0) and z > 50 and not (abs(x) < 23 and 59 < z < 71) and not (abs(x) < 37 and z < 56):
            out.append(e['mid'])                      # contorno frontal de la placa
        elif en(e, 2, 0) and y < ESP - 0.01:
            out.append(e['mid'])                      # base
        elif en(e, 2, 2):
            # canto del reborde del piso (convexo): lejos de las paredes
            lejos = (abs(abs(x) - AI / 2) > 3 and y < -3 and y > -FONDO_MAX(x))
            if lejos: out.append(e['mid'])
    return out

def FONDO_MAX(x):
    return PROF - 3 if abs(x) > HF / 2 else 1e9

if __name__ == '__main__':
    E = json.load(open(sys.argv[1]))
    sel = exteriores(E)
    print(len(sel), file=sys.stderr)
    json.dump(sel, sys.stdout)
