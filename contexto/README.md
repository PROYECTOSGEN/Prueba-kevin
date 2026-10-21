# contexto/

**Todo lo que se LEE para entender este proyecto.** Guías, actas de reunión,
transcripciones, criterios, referencias, decisiones del cliente.

## La regla, y es una cuenta, no un criterio

**Aquí van archivos sueltos con nombre descriptivo.** No carpetas por tema.

```
contexto/
├── guia-como-se-dimensiona-una-obra.md
├── 2026-09-07-reunion-continuidad.md
├── criterios-del-cliente.md
└── transcripciones/          ← serie de 27 dailies: esto SÍ es carpeta
```

**Una subcarpeta solo se justifica si es una SERIE que crece con el tiempo y ya
pasa de cinco piezas** — transcripciones, actas, dailies. Por debajo de cinco,
archivos sueltos.

**Por qué esa cuenta.** Con uno o dos archivos la carpeta cuesta más de lo que
ordena: hay que abrirla para descubrir que casi no tiene nada. Se puso un número
para que no se discuta cada vez.

Esto se midió: el 2026-09-21 había en los proyectos una carpeta `entregables`
con **un** archivo, una `guias` con **uno**, el mismo documento duplicado en dos
proyectos con tamaños distintos, y una `docs` con dos numeraciones encima
(`01_ARQUITECTURA` y `02_ARQUITECTURA`, `03_ROADMAP` y `05_ROADMAP`). No fue
desorden de las personas: fue que nadie había escrito esta regla.

## Lo que nunca va aquí

**Binarios.** PDF, video, planos, ZIP, Word, Excel → **Drive**. Aquí queda la
ficha en markdown que dice qué es y dónde está. Un repositorio de Git no es un
disco: cada versión de un archivo pesado se queda dentro del historial para
siempre, aunque después se borre.

**Código.** Eso va en `desarrollos/`.
