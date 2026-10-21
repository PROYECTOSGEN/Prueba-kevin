# <NOMBRE DEL PROYECTO> — criterio de este repositorio

> **Este archivo nació de una plantilla.** Todo lo que esté entre `<…>` o diga
> `POR_DEFINIR` hay que llenarlo antes del primer trabajo real. Si encuentras
> alguno de esos marcadores todavía puesto, **el repositorio no está terminado**:
> dilo y no sigas como si lo estuviera.

**Este repositorio es UN proyecto.** No es un área, no es un cajón general y no
es el sitio donde dejar algo que no supiste dónde va. Aquí vive el contexto, las
guías, las reuniones y los desarrollos de `<NOMBRE DEL PROYECTO>`, y nada más.

## Antes que nada: no se entra por aquí

**La puerta de entrada de todas las obras es el índice de `genplus-proyectos-contexto/00_Empresa`.**
Ahí está el índice que dice qué proyectos existen, dónde vive cada uno y quién
debe verlo. Se entra por el índice y desde ahí se viene al repositorio que
corresponde — no al revés.

**Si llegaste directo a este repositorio sin haber leído ese índice, léelo
ahora.** No es una formalidad: el índice es lo que evita que se abra un proyecto
que ya existe con otro nombre, que se trabaje en el repositorio equivocado, o
que se duplique algo que ya estaba resuelto en otro lado. Sin esa parada, cada
persona arma su propio mapa y en un mes nadie encuentra nada.

Al terminar, **si algo de este proyecto cambia de estado** —se cierra, cambia de
responsable, se suma un desarrollo—, eso se refleja en el índice de `00_Empresa`.
Un índice que miente es peor que no tenerlo.

## Qué es este proyecto

| | |
|---|---|
| Nombre | `<NOMBRE DEL PROYECTO>` |
| Cliente | `POR_DEFINIR` |
| Estado | `POR_DEFINIR` (activo · en pausa · cerrado) |
| Responsable | `POR_DEFINIR` |
| Abierto el | `POR_DEFINIR` |

## La estructura de este repositorio

**Tres carpetas en la raíz. Ni una más.**

| Carpeta | Qué va |
|---|---|
| `contexto/` | lo que se **lee** para entender el proyecto |
| `desarrollos/` | lo que se **ejecuta**; el código en `<nombre>/app/` |
| `one-context/` | `destino.json` |

Más los archivos de raíz: `_index.md`, `AGENTS.md`, `CLAUDE.md`, `README.md`,
`.gitignore`. **Nada suelto fuera de eso.**

**Dentro de `contexto/` van archivos, no carpetas por tema.** Una subcarpeta solo
si es una serie que crece con el tiempo y ya pasa de cinco piezas
(transcripciones, actas). Antes de cinco, archivos sueltos con nombre
descriptivo. Cada carpeta tiene su README con la regla completa.

**Si dudas dónde va algo, la pregunta no es de qué trata: es qué se hace con
ello.** ¿Se lee para entender? `contexto/`. ¿Se ejecuta? `desarrollos/`. ¿Es un
binario? No va al repositorio: va a Drive.

## Antes de empezar: el reporte de One Context

**Si lo que te piden deja algo guardado o publicado** —un HTML, un script, una
automatización, un documento, un archivo para Drive, un despliegue—, **antes de
escribir nada** resuelve dónde va y díselo a la persona.

**1 · Lee el destino.** `one-context/destino.json`, en la raíz de este
repositorio, dice dónde va lo de este proyecto: la carpeta de GitHub, el Vercel
y la carpeta de Drive. Las reglas comunes están en
`one-context/reglas-comunes.json` del repositorio `00_Empresa`, y quién puede hacer
qué, en `one-context/roles.json` del mismo. Si no puedes leer alguno, **dilo y
detente**: no reconstruyas el destino de memoria.

**2 · Clasifica lo que vas a hacer.** Un desarrollo —un HTML, un script, una
automatización o una aplicación que se compila— va en `desarrollos/<nombre>/`,
con el código en `app/`, su `README.md` y su ficha `desarrollo.json` (nombre,
estado, tipo, área, qué hace, despliegue). Un documento de trabajo va a `contexto/`: archivos sueltos, y una subcarpeta solo si es una serie
de más de cinco piezas. Un binario (PDF, video, Word, Excel) va a Drive y aquí queda su ficha.
**Nada suelto en la raíz.**

**Detente y pregunta** antes de escribir si el desarrollo necesita llaves de
servidor o va a guardar datos personales: **todo el equipo que tiene acceso a
este repositorio lo va a ver**, y ese acceso es más acotado que el de un
repositorio de área justamente porque este proyecto tiene su propia lista.

**3 · Mira con qué estás conectado.** Qué cuenta de GitHub, de Vercel y de
Drive tiene tu herramienta. Tiene que ser la **cuenta propia** de la persona.
`teamdev-genplus` es de administración: no se usa para desarrollar.

**4 · Muestra el reporte**: lo que pide el destino, lo que había, lo que moviste
y lo que no pudiste.

```text
ONE CONTEXT · arranque
Tarea:     <qué se va a hacer>
ÍNDICE     leído en genplus-proyectos-contexto/00_Empresa · este proyecto figura como <…>
GITHUB     pide <repo/ruta> · tenías <…> · → listo | moví a <…> | NO PUDE: <por qué>
VERCEL     pide <equipo> · tenías <…> · → …
DRIVE      pide <carpeta> · conectado como <cuenta> · → …
RESULTADO: arranco | me detengo hasta que se resuelva <…>
```

**Te detienes, y lo dices, si:** el destino dice `POR_DEFINIR`, `POR_CONECTAR`,
`POR_REVISAR`, `POR_MAPEAR` o `SIN_ACCESO` para lo que necesitas; la cuenta
conectada no corresponde o no tiene permiso; tendrías que crear un repositorio,
un proyecto de Vercel o una carpeta de Drive que el destino no nombra; o el
README de un desarrollo te manda a un lugar distinto del destino — **gana el
destino**, y preguntas.

**Si te piden crear un repositorio o un proyecto nuevo**, no improvises el nombre ni el lugar: sigue
`00_Empresa/one-context/crear-un-repositorio.md`. El nombre sale de la regla `nomenclatura_de_repositorios`
de `00_Empresa/one-context/reglas-comunes.json` y el número, de `00_Empresa/one-context/mapa.json`, que
es el mapa de toda la organización.

**«No pude» nunca se resuelve con una cuenta que sí puede.**

## Los archivos de este proyecto no se reparten por ahí

Lo que está aquí está aquí porque **alguien decidió quién puede verlo**. Antes
de copiar contenido de este repositorio a otro, a un chat, a un documento
compartido o a una herramienta de IA que no sea la de la persona, **pregunta**.
El límite de este repositorio es el límite de quién debe saber.

Y al revés: **no traigas aquí contenido de otro proyecto** para «tenerlo a
mano». Si hace falta referenciarlo, se enlaza por el índice.

## Crear otro repositorio

No se crea desde aquí sin leer antes `one-context/roles.json` de `00_Empresa`.
Ahí está quién está autorizado, y la regla que no tiene excepciones: **en esta
organización los repositorios son siempre privados.** Si tu herramienta ofrece
crearlo público, detente.

## Un guardián revisa cada push

Si algo queda fuera de lugar —un archivo suelto en la raíz, código fuera de
`app/`, un desarrollo sin ficha, un binario, llaves o un `.vercel/`—, el commit
queda en rojo y se abre un aviso en Issues. No bloquea: se corrige con un commit
nuevo. Que no marque nada **no reemplaza al reporte**, porque no ve Drive ni
Vercel.
