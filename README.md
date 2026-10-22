# Soporte de celular para pared

Soporte para pegar en la pared con cinta doble faz, diseñado en OpenSCAD.
Abierto por el frente y por abajo (para el cable de carga), con el nombre
**MOISES** calado en JetBrains Mono Bold y un patrón de puntos en degradado
en la placa trasera.

## Medidas

| | mm |
|---|---|
| Interior del bolsillo (ancho × profundidad) | 86 × 16 |
| Pieza completa (ancho × fondo × alto) | 90 × 20.5 × 80 |
| Grosor paredes / placa trasera | 2.0 / 2.5 |
| Celular con funda que entra | hasta 83 × 14 |

Todas las medidas son parámetros al inicio de `soporte.scad`.

## Generar el modelo

Necesita OpenSCAD nightly (2024 o más nuevo) con el motor **Manifold**:
renderiza en ~2 s, frente a ~17 min con el motor CGAL de la 2021.01.

```bash
make            # genera soporte.3mf
```

Se exporta en **3MF** porque conserva la malla exacta; el STL pierde
precisión y deja la pieza con errores. El archivo listo también está en las
[releases](../../releases).

## Impresión (Bambu Lab A1, PLA)

- De pie, tal como se cuelga (la espalda plana sobre la pared): **sin soportes**.
- Altura de capa 0.2 mm, 3 paredes, relleno 15–20 %.

## Montaje

La espalda tiene 4 rebajes de 0.5 mm para la cinta doble faz: arriba del
nombre, abajo y a los dos costados. No pongas cinta detrás de los puntos.

## Fuente

Requiere *JetBrainsMono Nerd Font* (Bold) instalada para generar el texto.
