// Soporte de celular para pared
// Se imprime de pie (como se cuelga): sin soportes.
// Vista frontal desde -Y. La espalda (y = espesor_espalda) va plana contra la pared.

/* [Medidas generales] */
alto_total        = 80;   // alto de la placa trasera (mm)
ancho_interior    = 86;   // ancho del bolsillo (celular con funda 83 + holgura)
profundidad       = 16;   // profundidad interior del bolsillo (celular con funda 14 + holgura)
alto_bolsillo     = 50;   // alto de la pared frontal del bolsillo
pared             = 2.0;  // grosor de paredes laterales, frontal y piso
espesor_espalda   = 2.5;    // grosor de la placa que va contra la pared
margen_placa      = 0;    // cuánto sobresale la placa a cada lado del bolsillo (0 = al ras)

/* [Redondeos] */
radio_placa_arriba = 12;  // esquinas superiores de la placa
radio_placa_abajo  = 1;   // esquinas inferiores de la placa
radio_bolsillo     = 7;   // esquinas frontales del bolsillo (vista desde arriba)
radio_bordes       = 0.9; // redondeo de todas las aristas (menor que pared/2, o la pared desaparece)
radio_filete       = 2;   // esquinas interiores entre laterales y placa
fn_bordes          = 40;  // resolución de los redondeos

/* [Huecos] */
ancho_hueco_frente = 56;  // abertura vertical en el frente
ancho_hueco_piso   = 40;  // abertura en el piso (para el cable)

/* [Texto] */
texto             = "MOISES";
fuente            = "JetBrainsMono Nerd Font:style=Bold";
alto_texto        = 9;    // altura de las letras
espaciado         = 0.78; // separación entre letras (proporción de alto_texto)
ancho_puente      = 2;    // puentes esténcil en letras cerradas (O, A, B...)
radio_letra       = 0.6;  // redondeo de las esquinas de las letras
radio_entrada     = 0.8;  // redondeo del borde del calado en la cara frontal
mostrar_texto     = true;

/* [Patrón de puntos] */
mostrar_patron    = true;
zona_z0           = 9;    // desde dónde empieza el patrón (deja banda para cinta abajo)
zona_z1           = 55;   // hasta dónde llega
paso_puntos       = 6.6;  // distancia entre puntos
radio_punto_max   = 2.9;  // puntos de abajo
radio_punto_min   = 0.8;  // puntos de arriba
filas_puntos      = 7;

/* [Rebajes para cinta doble faz (espalda)] */
mostrar_rebajes   = true;
profundidad_rebaje = 0.5;
radio_rebaje      = 1.5;  // esquinas de los rebajes

/* [Unión paredes-piso] */
radio_filete_piso = 2;    // filete cóncavo entre paredes/aletas y piso
pasos_filete      = 10;   // resolución del filete (capas)

$fn = 64;

ancho_ext   = ancho_interior + 2 * pared;
ancho_placa = ancho_ext + 2 * margen_placa;
fondo_total = profundidad + pared;          // lo que sobresale el bolsillo desde la placa
rb          = radio_bordes;
radio_esquinas = min(1, pared * 0.35);      // redondeo 2D de paredes y piso (< pared/2 o las borra)

// Redondea esquinas convexas y cóncavas de una figura 2D
module redondear(r) {
    offset(r = r) offset(delta = -r) offset(r = -r) offset(delta = r) children();
}

// Extruye una figura 2D en Z con todas las aristas redondeadas (radio rb)
module extruir_redondeado(alto) {
    translate([0, 0, rb])
        minkowski() {
            linear_extrude(alto - 2 * rb) offset(delta = -rb) children();
            sphere(rb, $fn = fn_bordes);
        }
}

// --- Perfiles 2D del bolsillo (plano XY, vista desde arriba) ---
module bolsillo_exterior() {
    hull() {
        for (s = [-1, 1])
            translate([s * (ancho_ext / 2 - radio_bolsillo), -fondo_total + radio_bolsillo])
                circle(radio_bolsillo);
        translate([-ancho_ext / 2, -1]) square([ancho_ext, 1 + espesor_espalda + 2 * rb]);
    }
}

module bolsillo_interior() {
    ri = radio_bolsillo - pared;
    hull() {
        for (s = [-1, 1])
            translate([s * (ancho_interior / 2 - ri), -profundidad + ri])
                circle(ri);
        // esquinas traseras con filete: unión suave entre laterales y placa
        for (s = [-1, 1])
            translate([s * (ancho_interior / 2 - radio_filete), -radio_filete])
                circle(radio_filete);
    }
}

module paredes_2d() {
    redondear(radio_esquinas)
        difference() {
            bolsillo_exterior();
            bolsillo_interior();
            translate([-ancho_hueco_frente / 2, -fondo_total - 1])
                square([ancho_hueco_frente, fondo_total + 1 - profundidad + 1]);
        }
}

module piso_2d() {
    redondear(radio_esquinas)
        difference() {
            bolsillo_exterior();
            // ranura del cable: abierta al frente, con el fondo redondo
            hull() {
                translate([-ancho_hueco_piso / 2, -fondo_total - 1]) square([ancho_hueco_piso, 1]);
                for (s = [-1, 1])
                    translate([s * (ancho_hueco_piso / 2 - 4), -2 - 4]) circle(4);
            }
        }
}

// --- Placa trasera (plano XZ) ---
module placa_2d() {
    hull() {
        for (s = [-1, 1]) {
            translate([s * (ancho_placa / 2 - radio_placa_abajo), radio_placa_abajo])
                circle(radio_placa_abajo);
            translate([s * (ancho_placa / 2 - radio_placa_arriba), alto_total - radio_placa_arriba])
                circle(radio_placa_arriba);
        }
    }
}

module placa() {
    // se hace más gruesa, se redondea y se corta plana por detrás
    intersection() {
        translate([0, espesor_espalda + rb, 0])
            rotate([90, 0, 0])
                translate([0, 0, rb])
                    minkowski() {
                        linear_extrude(espesor_espalda + rb - 2 * rb) offset(delta = -rb) placa_2d();
                        sphere(rb, $fn = fn_bordes);
                    }
        translate([-ancho_placa, -1, -1]) cube([2 * ancho_placa, espesor_espalda + 1, alto_total + 2]);
    }
}

// Letras una por una (monoespaciado) para poder ubicar los puentes de cada letra
function x_letra(i) = (i - (len(texto) - 1) / 2) * alto_texto * espaciado;
letras_cerradas = "ABDOPQR04689";

// Letras con esquinas redondeadas; el redondeo va después de los puentes,
// así los extremos cortados por los puentes también quedan redondos.
module letras_2d() {
    offset(r = radio_letra) offset(delta = -radio_letra)
    offset(r = -radio_letra * 0.7) offset(delta = radio_letra * 0.7)
        difference() {
            for (i = [0 : len(texto) - 1])
                translate([x_letra(i), 0])
                    text(texto[i], size = alto_texto, font = fuente, halign = "center", valign = "center");
            // puentes verticales: unen el centro de la letra con la placa
            for (i = [0 : len(texto) - 1])
                if (len(search(texto[i], letras_cerradas)) > 0)
                    translate([x_letra(i), 0]) square([ancho_puente, alto_texto * 2], center = true);
        }
}

// Corte que atraviesa la placa con la figura 2D (plano XZ), con la entrada frontal redondeada
module cortar_con_entrada() {
    rr = radio_entrada;
    n = 8;
    translate([0, espesor_espalda + 1, 0])
        rotate([90, 0, 0])
            linear_extrude(espesor_espalda + 2)
                children();
    // capas finas cerca de la cara frontal: el hueco se ensancha en curva hacia afuera
    for (k = [0 : n - 1]) {
        t0 = k * rr / n;
        t1 = (k + 1) * rr / n;
        w = rr - sqrt(rr * rr - (rr - t0) * (rr - t0));
        y0 = k == 0 ? -1 : t0;
        translate([0, t1, 0])
            rotate([90, 0, 0])
                linear_extrude(t1 - y0)
                    offset(r = w) children();
    }
}

// El calado del nombre
module calado() {
    cortar_con_entrada()
        translate([0, (alto_bolsillo + alto_total) / 2]) letras_2d();
}

// Filete cóncavo sobre el piso, al pie de paredes y aletas (por capas)
module filete_piso() {
    rf = radio_filete_piso;
    intersection() {
        for (k = [0 : pasos_filete - 1]) {
            h0 = k * rf / pasos_filete;
            h1 = (k + 1) * rf / pasos_filete;
            d = rf - sqrt(rf * rf - (rf - h1) * (rf - h1));
            translate([0, 0, pared - 0.01 + h0])
                linear_extrude(h1 - h0 + 0.01)
                    offset(r = d) paredes_2d();
        }
        // solo sobre el piso (sin invadir la ranura ni los bordes redondeados)
        linear_extrude(pared + rf + 1) offset(delta = -rb) piso_2d();
    }
}

// Puntos calados en degradado: grandes abajo, pequeños arriba, en tresbolillo.
// Deja ~9 mm libres a los lados y abajo para la cinta.
module puntos_2d() {
    zona_x = ancho_interior / 2 - 7;
    for (iz = [0 : filas_puntos - 1]) for (ix = [-6 : 6]) {
        x = ix * paso_puntos + (iz % 2) * paso_puntos / 2;
        z = zona_z0 + 3 + iz * paso_puntos;
        r = radio_punto_min + (radio_punto_max - radio_punto_min) * (1 - iz / (filas_puntos - 1));
        if (abs(x) + r <= zona_x && z + r <= zona_z1) translate([x, z]) circle(r = r, $fn = 32);
    }
}

module patron() {
    cortar_con_entrada() puntos_2d();
}

// Rebajes en la espalda para la cinta: arriba del nombre, abajo y a los costados
// (fuera de los puntos y del nombre, con ~2 mm de borde sin rebajar)
module rebajes_2d() {
    xp = ancho_interior / 2 - 7;                // ancho de la zona de puntos
    xc = xp + 1.5;                              // los costados empiezan tras los puntos
    xb = ancho_placa / 2 - 2;                   // borde exterior
    module rect(x0, z0, x1, z1) {
        offset(r = radio_rebaje) offset(delta = -radio_rebaje)
            translate([x0, z0]) square([x1 - x0, z1 - z0]);
    }
    rect(-24, 72, 24, 77);                      // arriba del nombre
    rect(-xp, 2, xp, 8);                        // abajo
    for (s = [-1, 1]) mirror([s < 0 ? 1 : 0, 0]) rect(xc, 11, xb, 60); // costados
}

module rebajes() {
    translate([0, espesor_espalda + 1, 0])
        rotate([90, 0, 0])
            linear_extrude(1 + profundidad_rebaje) rebajes_2d();
}

module soporte() {
    // el patrón se resta de todo: placa y la parte del bolsillo que queda dentro de la placa
    difference() {
        union() {
            difference() {
                placa();
                if (mostrar_texto) calado();
            }
            // los laterales llegan hasta la espalda y se cortan planos: quedan al ras con la placa
            intersection() {
                union() {
                    extruir_redondeado(alto_bolsillo) paredes_2d();
                    extruir_redondeado(pared) piso_2d();
                    filete_piso();
                }
                translate([-ancho_placa, -fondo_total - 1, -1])
                    cube([2 * ancho_placa, fondo_total + 1 + espesor_espalda, alto_total + 2]);
            }
        }
        if (mostrar_patron) patron();
        if (mostrar_rebajes) rebajes();
    }
}

soporte();
