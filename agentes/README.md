# agentes/ — los agentes de esta área

Un **agente** es algo a lo que le encargas un trabajo y vuelve con el resultado. Aquí viven
**todos** los del área, de los dos tipos que existen:

- **Los que corren solos en un servidor** y atienden a alguien —un bot de WhatsApp, un proceso
  que contesta consultas—. Siguen funcionando con tu computadora apagada.
- **Los que lanza tu IA** cuando se lo pides —«revisá esta cotización buscándole agujeros»— y
  vuelven con un informe. Corren en tu máquina, cuando tú los llamas.

**Los dos se guardan igual y en el mismo sitio.** Lo que cambia es un campo de la ficha, y lo
que tu IA hace con él al instalarlo.

## Qué lleva cada agente

```
agentes/<nombre>/
├── agente.json     ← la ficha: qué hace, de qué tipo es, qué necesita
├── prompt.md       ← sus instrucciones, completas
├── README.md       ← cómo se prueba y a quién avisar si falla
└── <nombre>.env    ← sus llaves (solo si corre en un servidor)
```

La ficha, con el campo que decide todo:

```json
{
  "nombre": "mariana",
  "tipo": "desplegado",
  "que_hace": "atiende consultas de ventas por WhatsApp",
  "estado": "produccion",
  "donde_corre": "n8n en el VPS",
  "responsable": "POR_DEFINIR",
  "variables_requeridas": ["EVOLUTION_API_KEY", "OPENAI_API_KEY"]
}
```

```json
{
  "nombre": "auditor-de-cotizaciones",
  "tipo": "subagente",
  "que_hace": "revisa una cotización antes de enviarla: alcance sin precio, unidades que no cierran",
  "estado": "activo",
  "herramientas": ["Read", "Grep", "Glob"],
  "vuelve_con": "una lista de hallazgos con evidencia, sin editar nada"
}
```

**`tipo` acepta dos valores y solo dos: `desplegado` o `subagente`.** La pregunta que los
separa: **¿sigue funcionando con tu computadora apagada?** Sí → `desplegado`. No → `subagente`.

En un `subagente`, **`herramientas` es un freno, no un adorno.** Si solo le das lectura, no
puede tocar un archivo aunque se equivoque. Si tiene que dejar un informe, agrégale escritura.

## Cómo lo usas, según con qué trabajes

Un agente **desplegado** no se instala: ya está corriendo. Aquí está su documentación y su
configuración para que puedas operarlo.

Un **subagente** sí, y cada herramienta lo quiere en su propia carpeta y **en su propio
formato**. Por eso lo guardamos aquí en formato neutro. **Pídeselo a tu IA así:**

> «Instala el subagente `agentes/<nombre>/` en la ruta y el formato que tú usas.»

| Tu herramienta | A dónde va | En qué formato |
|---|---|---|
| **Claude Code** | `.claude/agents/<nombre>.md` | Markdown con `name`, `description`, `tools` |
| **Codex** | `.codex/agents/<nombre>.toml` | TOML con `name`, `description`, `developer_instructions` |
| **ChatGPT web (conector)** | a ningún lado | ahí no se lanzan solos; pégale el `prompt.md` |

Las instrucciones exactas —qué campo va en cuál— están en `00_Empresa/AGENTS.md`, sección «Cómo
instalas una capacidad». Tu IA ya las tiene: lee ese archivo al abrir el repositorio.

**Después de instalar, `.claude/` y `.codex/` no se suben.** Son tu copia de trabajo.

## Las llaves: aquí sí van, y se usan sin leerlas

**En esta organización el `.env` de un agente desplegado se versiona a propósito** (decisión del
2026-09-26): quien tiene acceso al repositorio puede **usar** el agente sin ir a pedirle
credenciales a nadie.

**La regla de uso es una sola: se pasa como referencia, nunca se abre para mostrar su
contenido.**

| Esto sí | Esto no |
|---|---|
| `docker run --env-file mariana.env …` | abrirlo y mostrar sus líneas |
| `source mariana.env && ./correr.sh` | copiar un valor al chat, aunque sea «para verificar» |
| decir *«usé `mariana.env`»* | decir *«la clave es `sk-…`»* |
| nombrar **qué** variable falta | imprimir **qué valor** tiene |

**Para saber si una variable existe sin revelarla:** `grep -c '^EVOLUTION_API_KEY=' mariana.env`
devuelve 1 o 0.

**El `.env` va DENTRO de la carpeta del agente.** Nunca suelto en la raíz, y nunca dentro de
`app/` — `app/` es lo que se despliega, así que un `.env` ahí sale al servidor. El guardián
marca los dos casos.

**Un subagente no lleva llaves.** Corre en tu máquina, con tus credenciales.

## Lo único prohibido sin excepción

Que un repositorio con llaves **se vuelva público**. Si pasa, no alcanza con sacar el archivo:
hay que **rotar** todas las llaves que contenía, porque lo que estuvo público ya pudo copiarse.

## Cómo registras uno nuevo

1. `agentes/<nombre>/` con su `agente.json` —**con el campo `tipo`**— y su `prompt.md`
2. El `README.md` con cómo se prueba y a quién avisar si falla
3. Su `.env` si es desplegado, **dentro de esa carpeta**
4. **Agrégalo al catálogo:** `00_Empresa/skills/_index.md`

## Qué NO es un agente

- Una **instrucción** que cambia cómo trabajas tú → `skills/<nombre>/`
- Un **script** que corres a mano → `desarrollos/<nombre>/app/`
- Una **automatización sin conversación** (un workflow que solo mueve datos) → es un desarrollo

## La regla que ahorra discusiones

**Si lo usaría alguien de otra área, va en `00_Empresa`. Si solo esta área, va aquí.**
