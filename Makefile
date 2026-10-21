OPENSCAD ?= openscad

soporte.stl: soporte.scad
	$(OPENSCAD) -o $@ $<

clean:
	rm -f soporte.stl

.PHONY: clean
