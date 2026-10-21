# -*- coding: utf-8 -*-
"""One Context — freno de estructura.

Se ejecuta ANTES de cada escritura y detiene la que quedaria fuera del esquema.
Recibe por entrada estandar el JSON que manda la herramienta y devuelve:

    0  ->  la escritura sigue
    2  ->  la escritura se detiene, y el motivo va por error estandar

El motivo NO es un regano: dice a donde iba la cosa. Una IA que lo lee suele
reubicar el archivo sola y seguir trabajando.

Vale para cualquier herramienta que mande {"tool_input": {"file_path": ...}}.
Si el JSON no trae ruta, deja pasar: este freno cuida la estructura, nada mas.
"""
import json
import os
import sys

# Las UNICAS carpetas de la raiz de un repositorio de One Context.
CARPETAS_DE_RAIZ = {
    "contexto",      # el criterio: lo que se lee
    "desarrollos",   # lo que se ejecuta, cada uno en desarrollos/<nombre>/app/
    "skills",        # instrucciones que la IA lee para trabajar mejor
    "agentes",       # agentes, con su ficha y su prompt
    "one-context",   # la configuracion del repositorio
    ".github",       # el guardian y los flujos
    ".claude",       # el enganche de este mismo freno
}

# Los UNICOS archivos sueltos que admite la raiz.
ARCHIVOS_DE_RAIZ = {
    "AGENTS.md", "CLAUDE.md", "README.md", "_index.md",
    ".gitignore", ".gitattributes",
}

DONDE_VA = (
    "Si es criterio para leer, va en `contexto/`.\n"
    "Si se ejecuta, va en `desarrollos/<nombre>/app/`.\n"
    "Si es una instruccion para tu IA, va en `skills/<nombre>/`.\n"
    "Si es un agente, va en `agentes/<nombre>/`.\n"
    "Lo demas —documentos, imagenes, videos— va a Drive; aqui queda su ficha.\n"
    "El detalle esta en AGENTS.md, seccion «Como se estructura un repositorio»."
)


def main():
    try:
        datos = json.load(sys.stdin)
    except Exception:
        return 0  # sin datos utiles no se bloquea nada

    entrada = datos.get("tool_input") or {}
    ruta = entrada.get("file_path") or entrada.get("path") or ""
    if not ruta:
        return 0

    base = datos.get("cwd") or os.getcwd()
    try:
        rel = os.path.relpath(ruta, base)
    except Exception:
        return 0
    if rel.startswith(".."):
        return 0  # fuera del repositorio: no es asunto de esta regla

    partes = rel.replace("\\", "/").split("/")

    if len(partes) == 1:
        if partes[0] in ARCHIVOS_DE_RAIZ:
            return 0
        sys.stderr.write(
            "One Context — la raiz no admite archivos sueltos.\n\n"
            "`%s` quedaria suelto en la raiz. Ahi solo van: %s.\n\n%s\n"
            % (partes[0], ", ".join(sorted(ARCHIVOS_DE_RAIZ)), DONDE_VA)
        )
        return 2

    if partes[0] not in CARPETAS_DE_RAIZ:
        sys.stderr.write(
            "One Context — `%s/` no es una carpeta de la raiz.\n\n"
            "Las unicas son: %s.\n\n%s\n"
            % (partes[0], ", ".join(sorted(CARPETAS_DE_RAIZ)), DONDE_VA)
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
