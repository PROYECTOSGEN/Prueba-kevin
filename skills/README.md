# skills/ — las capacidades de esta área

Una **skill** es una instrucción que tu IA usa cuando la tarea le corresponde: cómo se cotiza
aquí, cómo se arma una propuesta, qué se revisa antes de enviar algo a un cliente.

**Se guardan aquí, en una carpeta con nombre normal.** No en `.claude/`, no en `.agents/`, no en
ninguna carpeta que pertenezca a una herramienta. El motivo está abajo, y es lo que hace que
esto sirva uses lo que uses.

## Cómo es una skill

```
skills/cotizar-servicio-bim/
├── SKILL.md        ← obligatorio
└── references/     ← opcional: material de apoyo
```

Y el `SKILL.md` empieza con su ficha:

```markdown
---
name: cotizar-servicio-bim
description: Usar cuando haya que armar una cotización de servicio BIM — definir alcance,
  unidades, precios de referencia y forma de pago. Incluye los ratios por tipo de servicio.
---

(aquí el criterio: cómo se hace, qué se decide, qué NO se hace)
```

**El `description` es lo que hace que funcione.** Tu IA lo lee y decide si abrir la skill. Una
descripción vaga —«ayuda con cotizaciones»— y la skill existe sin que nadie la use nunca.
Escríbela diciendo **cuándo** usarla, no qué contiene.

Este formato —carpeta con `SKILL.md`, `name` y `description`— es el mismo en Claude Code y en
Codex. Por eso una skill se guarda una sola vez y sirve para las dos.

## Cómo la usas, según con qué trabajes

Cada herramienta busca las skills en **su propia carpeta**, y ninguna deja cambiarla. Así que
las guardamos aquí y le dices a tu IA que las instale. **Pídeselo con estas palabras:**

> «Instala las skills de `skills/` en la ruta que tú usas.»

Lo que hará, según cuál sea:

| Tu herramienta | A dónde las lleva |
|---|---|
| **Claude Code** | `.claude/skills/` |
| **Codex** | `.agents/skills/` — en la raíz del repositorio |
| **ChatGPT web (conector)** | a ningún lado: ahí no se activan solas. Nómbrale el archivo que quieres que lea |

Las instrucciones exactas están en `00_Empresa/AGENTS.md`, sección «Cómo instalas una capacidad».
Tu IA ya las tiene: ese archivo lo lee al abrir el repositorio.

**Después de instalar, `.claude/` y `.agents/` no se suben.** Son tu copia de trabajo. Lo que
se versiona es esta carpeta.

## Cómo aportas la tuya

1. Crea `skills/<nombre-en-minusculas-con-guiones>/SKILL.md`
2. Escribe su `name` y su `description` — la descripción es el trabajo importante
3. Si necesita material extra, ponlo en `references/` dentro de su carpeta
4. **Agrégala al catálogo:** `00_Empresa/skills/_index.md`. Si no está ahí, existe y nadie la
   encuentra

## Qué NO va aquí

- **Un agente** —algo a lo que le delegas un trabajo entero y vuelve con el resultado, o algo
  que corre solo en un servidor— va en `agentes/<nombre>/`
- **Código que se ejecuta** → `desarrollos/<nombre>/app/`
- **Binarios**: PDF, imágenes, videos → Drive
- **Una skill duplicada de otra área.** Si dos la necesitan, **sube a `00_Empresa`**: no se copia.
  Copiar es lo que hace que las dos versiones divergan y nadie sepa cuál vale

## La regla que ahorra discusiones

**Si la usaría alguien de otra área, va en `00_Empresa`. Si solo esta área, va aquí.**
