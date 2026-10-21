# -*- coding: utf-8 -*-
"""Regenera skills/_index.md leyendo lo que HAY en el repo.
   Corre en GitHub Actions cuando alguien toca skills/ o agentes/.
   Nadie escribe este indice a mano: se escribe solo."""
import os, re, json, io, glob

def frontmatter(ruta):
    try:
        t = io.open(ruta, encoding="utf-8").read()
    except Exception:
        return {}
    m = re.match(r'^\ufeff?---\s*\n(.*?)\n---\s*\n', t, re.S)
    if not m:
        return {}
    campos, clave = {}, None
    for linea in m.group(1).split("\n"):
        mm = re.match(r'^([A-Za-z_-]+):\s*(.*)$', linea)
        if mm:
            clave = mm.group(1).strip()
            val = mm.group(2).strip()
            campos[clave] = "" if val in (">-", ">", "|", "|-") else val.strip('"\'')
        elif clave and linea.startswith((" ", "\t")):
            campos[clave] = (campos[clave] + " " + linea.strip()).strip()
    return campos

def recortar(s, n=150):
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[:n-1].rsplit(" ", 1)[0] + "…"

area = os.environ.get("AREA", "esta área")

skills = []
for sm in sorted(glob.glob("skills/*/SKILL.md")):
    f = frontmatter(sm)
    nombre = f.get("name") or os.path.basename(os.path.dirname(sm))
    refs = len(glob.glob(os.path.join(os.path.dirname(sm), "references", "*")))
    skills.append((nombre, recortar(f.get("description", "")), os.path.dirname(sm).replace(os.sep, "/"), refs))

agentes = []
for aj in sorted(glob.glob("agentes/*/agente.json")):
    try:
        d = json.load(io.open(aj, encoding="utf-8"))
    except Exception:
        d = {}
    agentes.append((d.get("nombre") or os.path.basename(os.path.dirname(aj)),
                    d.get("tipo", "?"), recortar(d.get("que_hace", "")),
                    d.get("usa_skill", ""), os.path.dirname(aj).replace(os.sep, "/")))

L = []
L.append("# Capacidades de %s\n" % area)
L.append("> **Este archivo lo escribe una máquina.** Se regenera solo cada vez que alguien")
L.append("> toca `skills/` o `agentes/`. **No lo edites a mano:** tu cambio se pierde en el")
L.append("> siguiente push. Lo que sí controlas es el `description` de tu skill y el")
L.append("> `que_hace` de tu agente — de ahí sale cada fila.\n")

L.append("## Skills — %d\n" % len(skills))
if skills:
    L.append("| Skill | Cuándo se usa | Dónde |")
    L.append("|---|---|---|")
    for n, d, ruta, refs in skills:
        extra = " · %d referencias" % refs if refs else ""
        L.append("| **%s** | %s | [`%s/`](../%s/)%s |" % (n, d or "*(sin `description` — no se va a activar sola)*", ruta, ruta, extra))
else:
    L.append("*Todavía ninguna.* La primera va en `skills/<nombre>/SKILL.md`.")
L.append("")

L.append("## Agentes — %d\n" % len(agentes))
if agentes:
    L.append("| Agente | Tipo | Qué hace | Usa la skill | Dónde |")
    L.append("|---|---|---|---|---|")
    for n, tipo, q, us, ruta in agentes:
        L.append("| **%s** | `%s` | %s | %s | [`%s/`](../%s/) |" %
                 (n, tipo, q or "*(sin `que_hace`)*", ("`%s`" % us) if us else "—", ruta, ruta))
else:
    L.append("*Todavía ninguno.* El primero va en `agentes/<nombre>/` con su `agente.json`.")
L.append("")

L.append("## Cómo se usan\n")
L.append("Las carpetas `skills/` y `agentes/` **no son de ninguna herramienta**: cada quien las")
L.append("instala en la suya. Pídeselo a tu IA con estas palabras:\n")
L.append("> «Instala las skills de `skills/` y los subagentes de `agentes/` en la ruta y el")
L.append("> formato que tú usas.»\n")
L.append("Las instrucciones exactas están en `00_Empresa/one-context/capacidades.md`.\n")
L.append("**La regla de desempate:** si lo usaría otra área, va en `00_Empresa`. Si solo esta área,")
L.append("va acá. Nunca se copia entre áreas.")

io.open("skills/_index.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
print("indice regenerado: %d skills, %d agentes" % (len(skills), len(agentes)))
