# Soporte de celular para pared

Soporte para pegar en la pared con cinta doble faz, diseñado en
[SolidCraft](https://github.com/tangency-labs/solidcraft). Abierto por el frente y por abajo
(para el cable de carga), con un nombre calado en JetBrains Mono Bold (ahora **ERWIN**; se cambia en `solidcraft/nombre.py`), un patrón de
puntos en degradado en la placa trasera y una boca en forma de embudo para recibir el celular.

## Medidas

| | mm |
|---|---|
| Interior del bolsillo (ancho × profundidad) | 84.5 × 13 |
| Pieza completa (ancho × fondo × alto) | 91.9 × 19.2 × 80 |
| Alto de paredes + boca | 45.5 + 4.5 = 50 |
| Grosor paredes / placa trasera | 2.0 / 2.5 |
| Abertura frontal / ranura del piso | 66.5 / 56 |
| Celular con funda que entra | hasta 83 × 12 |

## Archivos

Todo el diseño está en `solidcraft/`:

- `soporte.solidcraft`: el diseño para abrir en la app.
- `soporte.json`: el script que lo reconstruye desde cero sin abrir la app (lo usa `make`).
- `todo.py`: reconstruye el soporte completo en una ventana abierta con
  `solidcraft --control 7878` (~3 min), guarda `soporte.solidcraft` y exporta `soporte.json`.
- `gen.py`, `boca.py`, `punta.py`, `nombre.py`: las medidas y los pasos que usa `todo.py`
  (medidas al inicio de cada uno). `nombre.py` pone un puente bajo el hueco de cada letra cerrada
  (A, D, O, R…), así que sirve para cualquier nombre.
- `live.py`: el cliente que maneja la ventana en vivo.

Para cambiar una medida o el nombre: edítalo en `gen.py`, `boca.py`, `punta.py` o `nombre.py` y corre
`python3 todo.py`.

## Generar el modelo

```bash
make            # soporte.step desde solidcraft/soporte.json (~2 min)
```

El archivo listo también está en las [releases](../../releases).

## Impresión (Bambu Lab A1, PLA)

- Abre el **STEP** en Bambu Studio: genera su propia malla desde las superficies exactas.
  El 3MF que exporta SolidCraft tiene pequeñas costuras abiertas.
- De pie, tal como se cuelga (la espalda plana sobre la pared): **sin soportes**, borde (brim) de 5 mm.
- Altura de capa 0.2 mm, 3 paredes, relleno 15–20 %.

## Montaje

La espalda tiene 4 rebajes de 0.5 mm para la cinta doble faz: arriba del nombre, abajo y a
los dos costados. No pongas cinta detrás de los puntos.

## Fuente

Requiere *JetBrainsMono Nerd Font* (Bold) instalada para generar el texto.

## Historia

Hasta la v1.1.0 el diseño principal estaba en OpenSCAD (`soporte.scad`); ese archivo sigue en el
historial de git y en los tags `v1.0.0`, `v1.0.1` y `v1.1.0`.
