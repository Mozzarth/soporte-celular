# Soporte de celular para pared

Soporte para pegar en la pared con cinta doble faz, diseñado en OpenSCAD.
Abierto por el frente y por abajo (para el cable de carga), con el nombre
**MOISES** calado en JetBrains Mono Bold y un patrón de puntos en degradado
en la placa trasera.

## Medidas

| | mm |
|---|---|
| Interior del bolsillo (ancho × profundidad) | 86 × 16 |
| Pieza completa (ancho × fondo × alto) | 90.8 × 21.4 × 80 |
| Celular con funda que entra | hasta 83 × 14 |

Todas las medidas son parámetros al inicio de `soporte.scad`.

## Generar el STL

```bash
make            # usa OpenSCAD instalado
```

o abre `soporte.scad` en OpenSCAD y exporta con F6 → *Export as STL*.
El STL listo también está en las [releases](../../releases).

## Impresión (Bambu Lab A1, PLA)

- De pie, tal como se cuelga (la espalda plana sobre la pared): **sin soportes**.
- Altura de capa 0.2 mm, 3 paredes, relleno 15–20 %.

## Montaje

La espalda tiene 4 rebajes de 0.5 mm para la cinta doble faz: arriba del
nombre, abajo y a los dos costados. No pongas cinta detrás de los puntos.

## Fuente

Requiere *JetBrainsMono Nerd Font* (Bold) instalada para generar el texto.
