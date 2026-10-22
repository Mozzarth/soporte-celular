# Requiere OpenSCAD 2024+ (nightly) para el motor Manifold: segundos en vez de ~17 min con CGAL
OPENSCAD ?= openscad-nightly

soporte.3mf: soporte.scad
	$(OPENSCAD) --backend=Manifold -o $@ $<

clean:
	rm -f soporte.3mf

.PHONY: clean
