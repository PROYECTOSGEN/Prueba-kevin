#!/usr/bin/env python3
"""One Context · guardián. Revisa lo que entró en un push y avisa si quedó fuera de lugar.

No bloquea (el plan de GitHub no permite proteger ramas en repositorios privados): deja el
commit en rojo y abre un aviso para quien lo subió. Las reglas son las del AGENTS.md de este
repositorio y de one-context/destino.json.

Uso:  python3 guardian.py --repo ORG/REPO --antes SHA --despues SHA   (lo que entró en el push)
      python3 guardian.py --repo ORG/REPO --completo                  (todo el repositorio)
"""
import argparse, json, os, re, subprocess, sys

RAIZ_ARCHIVOS = {"AGENTS.md", "CLAUDE.md", "README.md", "_index.md", ".gitignore", ".gitattributes"}
# REGLA DE RAIZ - tres carpetas, ni una mas (decision del 2026-09-21).
#   contexto/     lo que se LEE para entender el proyecto
#   desarrollos/  lo que se EJECUTA; el codigo en <nombre>/app/
#   one-context/  destino.json
# Dentro de contexto/ van ARCHIVOS sueltos con nombre descriptivo. Una subcarpeta SOLO si
# es una serie que crece con el tiempo y ya pasa de cinco piezas (transcripciones, actas).
# Una carpeta con uno o dos archivos no es estructura: es un archivo con una carpeta encima.
# `.claude/` lleva las skills del area: se activan solas en Claude Code al clonar el repo.
# `agentes/` lleva los agentes documentados, con su ficha, su prompt y su .env.
# Las dos se abrieron el 2026-09-26; antes cualquier carpeta fuera de esta lista daba rojo.
# Las capacidades se guardan con nombre NEUTRAL, no bajo la carpeta de una herramienta:
#   `skills/`  las skills del area (SKILL.md con name y description)
#   `agentes/` los agentes, los dos tipos, separados por el campo `tipo` de agente.json
# Cada quien las INSTALA en la ruta de su herramienta (.claude/, .codex/, .agents/), y esas
# copias de trabajo NO se versionan. Cambio del 2026-09-26: antes lo canonico era `.claude/`,
# que solo servia a Claude Code — Codex usa .agents/skills y .codex/agents, y con otro formato.
RAIZ_CARPETAS = {"contexto", "desarrollos", "one-context", ".github", "agentes", "skills", ".claude"}
EN_UN_DESARROLLO = {"README.md", "desarrollo.json", "app", "guias", "entregables", "archivos"}
FICHA_CLAVES = ("nombre", "estado", "tipo", "area", "que_hace", "despliegue")
DOCUMENTOS = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".zip", ".rar", ".7z", ".mp4", ".mov",
              ".avi", ".psd", ".ai", ".dwg", ".rvt", ".ifc", ".nwd", ".skp"}
IMAGENES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico"}
TEXTO_DE_APOYO = {".md", ".txt"}
LLAVES = re.compile(r"(^\.env(\..+)?$|\.env$|\.pem$|\.key$|\.p12$|\.pfx$|^id_(rsa|ed25519)|credential.*\.json$|"
                    r"service[-_]?account.*\.json$|^secrets?\.(json|ya?ml|toml)$)", re.I)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8").stdout


def archivos_que_entraron(antes, despues, completo):
    if completo or not antes or set(antes) == {"0"}:
        if not completo and git("rev-parse", "--verify", "-q", "origin/main").strip():
            base = git("merge-base", "origin/main", despues).strip()
            if base and base != despues:
                antes = base
            else:
                return [p for p in git("ls-tree", "-r", "--name-only", despues).splitlines() if p]
        else:
            return [p for p in git("ls-tree", "-r", "--name-only", despues or "HEAD").splitlines() if p]
    salida = []
    for linea in git("diff", "--name-status", "-M", antes, despues).splitlines():
        partes = linea.split("\t")
        if not partes or partes[0].startswith("D"):
            continue
        salida.append(partes[-1])
    return salida


def existe(ref, ruta):
    return subprocess.run(["git", "cat-file", "-e", f"{ref}:{ruta}"], capture_output=True).returncode == 0


def revisar(repo, rutas, ref):
    nombre_repo = repo.split("/")[-1]
    # el prefijo de orden (00_, 01_) no es parte del nombre: 00_Empresa se juzga como empresa
    nombre_repo = re.sub(r"^\d+_", "", nombre_repo).lower()
    hallazgos = []
    fichas_vistas = set()
    for ruta in sorted(set(rutas)):
        partes = ruta.split("/")
        base = partes[-1]
        ext = os.path.splitext(base)[1].lower()

        if ".vercel" in partes:
            hallazgos.append((ruta, "El enlace de Vercel (`.vercel/`) es de cada máquina y no se sube."))
            continue
        if LLAVES.search(base):
            # Decision del 2026-09-26: un archivo de llaves ES legitimo DENTRO de la carpeta de
            # su agente o su desarrollo — es lo que permite que quien tiene acceso lo use sin
            # pedirle credenciales a nadie. Sigue siendo error suelto en la raiz o dentro de app/,
            # donde nadie lo espera y se cuela en un despliegue.
            # La regla de uso esta en empresa/AGENTS.md: se pasa por REFERENCIA, no se abre.
            en_su_carpeta = (("agentes" in partes or "desarrollos" in partes) and "app" not in partes)
            if not en_su_carpeta:
                hallazgos.append((ruta, "Un archivo de llaves va DENTRO de la carpeta de su agente o desarrollo "
                                        "(`agentes/<nombre>/` o `desarrollos/<nombre>/`), nunca suelto en la raíz "
                                        "ni dentro de `app/`. Y se usa por referencia: no se abre para mostrar su "
                                        "contenido (ver `empresa/AGENTS.md`)."))
            continue
        if ext in DOCUMENTOS:
            hallazgos.append((ruta, "Es un documento o binario: va a la carpeta de Drive del área (one-context/destino.json) "
                                    "y aquí queda solo su ficha en `archivos/`."))
            continue
        if ext in IMAGENES and "app" not in partes and not ruta.startswith("identidad-y-marca/"):
            hallazgos.append((ruta, "Las imágenes solo van dentro del `app/` de un desarrollo; el resto va a Drive."))
            continue

        if partes[0] == ".github":
            continue
        if nombre_repo != "empresa":
            if len(partes) == 1 and base not in RAIZ_ARCHIVOS:
                hallazgos.append((ruta, "Archivo suelto en la raíz. En la raíz solo van AGENTS.md, CLAUDE.md, README.md, "
                                        "_index.md, one-context/ y el .gitignore."))
                continue
            if len(partes) > 1 and nombre_repo != "proyectos" and partes[0] not in RAIZ_CARPETAS:
                hallazgos.append((ruta, f"La carpeta `{partes[0]}/` no es de la raíz de un área: el criterio va en `contexto/` "
                                        "y lo que se ejecuta en `desarrollos/<nombre>/`."))
                continue
            if nombre_repo == "proyectos" and partes[0] == "desarrollos":
                hallazgos.append((ruta, "En `proyectos`, un desarrollo va dentro de su tema: `<tema>/desarrollos/<nombre>/`."))
                continue

        if "desarrollos" in partes:
            i = partes.index("desarrollos")
            esperado = 1 if nombre_repo == "proyectos" else 0
            if i != esperado:
                donde = "`<tema>/desarrollos/<nombre>/`" if nombre_repo == "proyectos" else "`desarrollos/<nombre>/` en la raíz"
                hallazgos.append((ruta, f"Un desarrollo va en {donde}."))
                continue
            if len(partes) == i + 2:
                # El README.md de la raiz de `desarrollos/` es metadata de la carpeta, no un
                # desarrollo: explica la regla justo donde se necesita.
                if base != "README.md":
                    hallazgos.append((ruta, "Archivo suelto en `desarrollos/`: cada desarrollo tiene su carpeta, "
                                            "`desarrollos/<nombre>/`, con el código en `app/`."))
                continue
            carpeta = "/".join(partes[: i + 2])
            sub = partes[i + 2]
            if sub not in EN_UN_DESARROLLO:
                hallazgos.append((ruta, f"Dentro de `{carpeta}/` solo van README.md, desarrollo.json, app/, guias/, "
                                        "entregables/ y archivos/. El código va en `app/`."))
                continue
            if sub in ("guias", "entregables", "archivos") and ext not in TEXTO_DE_APOYO:
                hallazgos.append((ruta, f"En `{sub}/` va texto (.md). El código va en `{carpeta}/app/`."))
                continue
            if carpeta not in fichas_vistas:
                fichas_vistas.add(carpeta)
                if not existe(ref, f"{carpeta}/desarrollo.json"):
                    hallazgos.append((carpeta + "/", "El desarrollo no tiene su ficha `desarrollo.json` (nombre, estado, tipo, "
                                                     "área, qué hace y dónde se despliega)."))
                else:
                    try:
                        ficha = json.loads(git("cat-file", "blob", f"{ref}:{carpeta}/desarrollo.json"))
                        faltan = [k for k in FICHA_CLAVES if k not in ficha]
                        if faltan:
                            hallazgos.append((f"{carpeta}/desarrollo.json", "A la ficha le faltan campos: " + ", ".join(faltan) + "."))
                    except Exception:
                        hallazgos.append((f"{carpeta}/desarrollo.json", "La ficha no es un JSON válido."))
                if not existe(ref, f"{carpeta}/README.md"):
                    hallazgos.append((carpeta + "/", "El desarrollo no tiene `README.md` (qué es, cómo se usa, cómo se despliega)."))
    return hallazgos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--antes", default="")
    ap.add_argument("--despues", default="HEAD")
    ap.add_argument("--completo", action="store_true")
    ap.add_argument("--autor", default="")
    a = ap.parse_args()
    rutas = archivos_que_entraron(a.antes, a.despues, a.completo)
    hallazgos = revisar(a.repo, rutas, a.despues)
    alcance = "todo el repositorio" if a.completo else f"{len(rutas)} archivo(s) que entraron en `{a.despues[:7]}`"
    if not hallazgos:
        print(f"### One Context · guardián: todo en su lugar\n\nRevisado: {alcance}.")
        return 0
    quien = f"@{a.autor} " if a.autor and not a.completo else ""
    print(f"### One Context · guardián: {len(hallazgos)} cosa(s) fuera de lugar\n")
    print(f"{quien}Revisado: {alcance}. El commit ya está subido: el guardián no lo bloquea, avisa. "
          "Corrígelo con un commit nuevo y, si lo subió una IA, pídele que muestre antes el reporte de One Context "
          "(AGENTS.md, «Antes de empezar»).\n")
    print("| Archivo | Qué pasa |\n|---|---|")
    for ruta, motivo in hallazgos:
        print(f"| `{ruta}` | {motivo} |")
    return 1


if __name__ == "__main__":
    sys.exit(main())
