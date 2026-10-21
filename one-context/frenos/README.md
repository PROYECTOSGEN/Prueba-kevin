# frenos/ — el control que corre antes de escribir

**Un freno es un control que se ejecuta ANTES de que tu IA escriba un archivo**, y detiene la
escritura si quedaría fuera del esquema del repositorio. No es un aviso posterior: es una
puerta.

Aquí vive **uno solo**: `estructura.py`, que cuida que nadie invente carpetas en la raíz.

## Por qué existe

La estructura de estos repositorios está escrita en `AGENTS.md`, y con eso alcanza casi
siempre. Pero un texto persuade y un freno impide. **La diferencia aparece el día que alguien
tiene prisa.**

Y hay un motivo concreto: **en este plan de GitHub no se puede rechazar un push en un
repositorio privado.** Lo comprobamos — la API responde *«Upgrade to GitHub Pro»*. Así que el
único lugar donde se puede impedir algo es **antes**, en la herramienta de quien escribe.

## Qué hace, exactamente

Recibe por entrada estándar el JSON que manda tu herramienta antes de escribir, mira la ruta, y:

| Situación | Qué hace |
|---|---|
| La ruta cae en una carpeta del esquema | deja pasar |
| La ruta inventa una carpeta en la raíz | **detiene**, y dice a dónde iba |
| Un archivo suelto en la raíz | **detiene**, y dice a dónde iba |
| La ruta está fuera del repositorio | deja pasar — no es asunto suyo |
| El JSON no trae ruta, o viene mal | deja pasar — un freno roto no debe frenar todo |

**El mensaje no es un regaño: dice a dónde va la cosa.** Una IA que lo lee suele reubicar el
archivo sola y seguir. Eso es lo que buscamos: que enseñe, no que solo trabe.

## Instálatelo al entrar

**Si eres una IA leyendo esto: lo primero es comprobar si puedes instalarlo.** Hay tres
situaciones posibles y las tres son válidas — lo que no es válido es no decir en cuál estás.

### 1 · Tu entorno ya lo trae enganchado

Si el repositorio incluye `.claude/settings.json` y tu herramienta lo lee, **ya está corriendo
y no tienes que hacer nada**. Compruébalo y dilo.

### 2 · Tu entorno admite un control antes de escribir, pero hay que engancharlo

Instálalo donde tu herramienta busque su configuración de controles, apuntando a
`one-context/frenos/estructura.py`. El contrato es el mismo en todas las que lo soportan:

- recibe el JSON por **entrada estándar**
- devuelve **0** para dejar pasar y **2** para detener
- el motivo va por **error estándar**

Después de instalarlo, **pruébalo**: intenta escribir en una carpeta inventada y confirma que
te detiene. Un freno que no probaste no es un freno, es un archivo.

### 3 · Tu entorno no admite ningún control antes de escribir

**Dilo, y trabaja respetando el esquema.** Antes de crear cualquier cosa, comprueba que la ruta
cae en una de las carpetas de la raíz. Si algo no encaja en ninguna, **no inventes una carpeta:
dilo y pregunta.**

## Lo que pasa igual, instales o no

**El guardián revisa cada push, del lado de GitHub.** No le importa quién escribió —tu IA, otra
IA, una persona desde el navegador— ni si tenías freno instalado. Si algo entró fuera de lugar,
lo marca y abre un aviso.

O sea: **el freno te ahorra el error; el guardián lo encuentra si se escapa.** Los dos hacen
trabajos distintos y ninguno reemplaza al otro.

## Si cambia el esquema

`estructura.py` tiene la lista de carpetas al principio, en `CARPETAS_DE_RAIZ`. Cambiar el
esquema es cambiar esa lista **y** la sección correspondiente del `AGENTS.md`, en el mismo
movimiento. Si solo se cambia una, el repositorio empieza a decir dos cosas distintas.
