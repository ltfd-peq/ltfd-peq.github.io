#!/usr/bin/env python3
"""Barra marcadores de rascunho no site publicado e endereços escritos à mão.

Uso:
    python3 -I scripts/checar_marcadores.py [public] [raiz_do_repositorio]

1. No HTML gerado (texto visível, atributos e JSON-LD; comentários HTML são ignorados):
   "[a confirmar]", "a confirmar", "a definir", "lorem ipsum", "em construção",
   "under development", "[decisão]", "TODO" (PLANO §3.4 e checklist [L] do §13).
2. Nas fontes (content/, data/, layouts/, assets/, i18n/): o endereço do site só pode
   aparecer em config/_default/hugo.toml (baseURL), para a migração de domínio
   trocar uma linha só (PLANO §9.8).
No CI, roda no build de produção; no PR, roda como aviso (--aviso).
"""
import re
import sys
from pathlib import Path

MARCADORES = re.compile(
    r"\[a confirmar\]|\ba confirmar\b|\ba definir\b|lorem ipsum|em constru[çc][ãa]o|under development|\[decis[ãa]o\]|\bTODO\b",
    re.IGNORECASE,
)
ENDERECOS = ("ltfd-peq.github.io", "ltfd.peq.coppe.ufrj.br")
FONTES = ("content", "data", "layouts", "assets", "i18n", "static")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    aviso = "--aviso" in sys.argv
    public = Path(args[0] if args else "public")
    raiz = Path(args[1] if len(args) > 1 else ".")
    problemas = []

    for html in sorted(public.rglob("*.html")):
        texto = re.sub(r"<!--.*?-->", "", html.read_text(encoding="utf-8"), flags=re.S)
        for m in MARCADORES.finditer(texto):
            trecho = texto[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")
            problemas.append(f"{html}: marcador '{m.group(0)}' … {trecho} …")

    for pasta in FONTES:
        for arq in sorted((raiz / pasta).rglob("*")):
            if not arq.is_file() or arq.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".avif", ".woff2", ".ico"}:
                continue
            conteudo = arq.read_text(encoding="utf-8", errors="ignore")
            for end in ENDERECOS:
                if end in conteudo:
                    problemas.append(f"{arq}: endereço do site escrito à mão ({end}); use relURL/absURL e o baseURL")

    for p in problemas:
        print(("AVISO " if aviso else "ERRO  ") + p)
    print(f"\n{len(problemas)} problema(s).")
    if problemas and not aviso:
        sys.exit(1)


if __name__ == "__main__":
    main()
