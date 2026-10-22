# Changelog

## v1.1.1

- Se deja de usar OpenSCAD: se quita `soporte.scad` y el diseño único es el de SolidCraft
  (`solidcraft/`). `make` genera ahora `soporte.step` con `solidcraft-cli`.
- Abertura frontal de 66 a 70 mm (aletas de 8 mm) para que se vea más el teléfono.
- Corrige las grietas de la malla (57-68 aristas abiertas en Bambu Studio):
  - La O se corta en dos mitades dejando el puente sin cortar, en vez de pegarle un bloque.
  - El corte interior de la boca arranca 0.1 mm dentro de la pared.
- `todo.py` reconstruye el diseño completo en la app; reemplaza a `build.py` y `bordes.py`.

## v1.1.0

- OpenSCAD: abertura frontal de 56 a 66 mm (aletas de 10 mm) y del piso de 40 a 56 mm.
- Nueva versión en SolidCraft (`solidcraft/`), con cambios que aún no están en OpenSCAD:
  - Piso hueco: queda un reborde de 6 mm que sigue las paredes y da la vuelta por detrás de las aletas.
  - Boca en forma de embudo para recibir el celular: paredes de 45.5 mm + boca de 4.5 mm (alto total
    50 mm, igual que antes) que se abre 2 mm al frente y a los lados, unida a la espalda, con el canto
    redondeado y las puntas redondeadas vistas de frente.
  - Corrige los rebajes de la cinta, que en el modelo de SolidCraft quedaban delante de la placa.
  - Redondeos de 0.9 mm en el contorno de la placa y el reborde del piso, 0.45 mm en la base.
- Para imprimir: `soporte-v1.1.0.step` (Bambu Studio lo importa y genera su propia malla).

## v1.0.1

- Paredes, aletas y piso de 2.4 a 2.0 mm; placa trasera de 3 a 2.5 mm (2.0 en los rebajes).
  Pieza de 90 × 20.5 × 80 mm y ~18 % menos plástico (22.1 cm³).
- Redondeo de bordes de 1.1 a 0.9 mm y redondeo 2D proporcional a la pared,
  para que las paredes finas no desaparezcan.
- Se genera con OpenSCAD nightly y el motor Manifold (segundos en vez de ~17 min).
- El modelo se publica en 3MF en lugar de STL.

## v1.0.0

Primera versión.

- Bolsillo de 86 × 16 mm interior para celular con funda (83 × 14 mm + holgura).
- Abierto por el frente (56 mm) y por abajo (ranura de 40 mm para el cable).
- Laterales integrados al ras con la placa trasera, bordes redondeados y filetes.
- Nombre MOISES calado en JetBrains Mono Bold, con puentes esténcil y entrada redondeada.
- Patrón de puntos calados en degradado en la placa trasera, con entrada redondeada.
- Cuatro rebajes de 0.5 mm en la espalda para cinta doble faz.
