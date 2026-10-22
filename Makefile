# El diseño vive en SolidCraft: solidcraft/soporte.json es el script que lo reconstruye.
SOLIDCRAFT ?= solidcraft-cli

soporte.step: solidcraft/soporte.json
	$(SOLIDCRAFT) run $< --out $@ --quiet

solidcraft/soporte.solidcraft: solidcraft/soporte.json
	$(SOLIDCRAFT) run $< --save $@ --quiet

clean:
	rm -f soporte.step

.PHONY: clean
