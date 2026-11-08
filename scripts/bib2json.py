#!/usr/bin/env python3
"""Converte bib/ltfd.bib (fonte das publicações, PLANO D2) em data/gerado/publicacoes.json,
lido pelo Hugo na página Artigos publicados. Roda antes do build (local e CI).

Uso:
    python3 -I scripts/bib2json.py [raiz_do_repositorio]

Erros (saída com código 1): chave ou DOI repetidos; campo obrigatório ausente; ano não
numérico; DOI fora do formato; membro citado em `membros` que não existe em data/membros/.
Aviso: membro listado em `membros` que não foi achado entre os autores.

O arquivo .bib segue o formato descrito no cabeçalho dele: UTF-8 direto, um campo por linha,
valores entre chaves. O parser abaixo só entende esse formato (sem @string nem concatenação).
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

OBRIGATORIOS = ("author", "title", "journal", "year", "escopo", "membros", "fonte", "verificado_em")
INTERNOS = ("escopo", "membros", "fonte", "verificado_em")  # campos do LTFD, fora da exportação
PARTICULAS = {"da", "de", "do", "dos", "das", "e", "van", "von", "der", "del", "di", "la", "le"}


def sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def ler_valor(texto: str, i: int):
    """Lê um valor {…} (com chaves aninhadas) ou um número a partir de texto[i]."""
    if texto[i] == "{":
        nivel, j = 0, i
        while j < len(texto):
            if texto[j] == "{":
                nivel += 1
            elif texto[j] == "}":
                nivel -= 1
                if nivel == 0:
                    return texto[i + 1:j], j + 1
            j += 1
        raise ValueError("chave não fechada")
    m = re.match(r"[0-9]+", texto[i:])
    if not m:
        raise ValueError(f"valor inesperado: {texto[i:i + 30]!r}")
    return m.group(0), i + m.end()


def ler_bib(texto: str):
    entradas = []
    for m in re.finditer(r"^@(\w+)\s*\{\s*([^,\s]+)\s*,", texto, flags=re.M):
        tipo, chave, i = m.group(1).lower(), m.group(2), m.end()
        campos = {}
        while True:
            while i < len(texto) and texto[i] in " \t\r\n,":
                i += 1
            if texto[i] == "}":
                break
            n = re.match(r"(\w+)\s*=\s*", texto[i:])
            if not n:
                raise ValueError(f"{chave}: campo malformado perto de {texto[i:i + 40]!r}")
            nome = n.group(1).lower()
            valor, i = ler_valor(texto, i + n.end())
            campos[nome] = " ".join(valor.split())
        entradas.append({"tipo": tipo, "chave": chave, "campos": campos, "bruto": texto[m.start():i + 1]})
    return entradas


def iniciais(prenome: str) -> str:
    partes = []
    for tok in prenome.split():
        if tok.lower() in PARTICULAS:          # "Fernando C. de" → "F. C. de"
            partes.append(tok.lower())
        elif tok.endswith(".") and len(tok) <= 3:
            partes.append(tok)
        else:
            partes.append("-".join(p[0] + "." for p in tok.split("-") if p))
    return " ".join(partes)


def autores(campo: str, membros: list, nomes_membros: dict, chave: str, avisos: list):
    lista, achados = [], set()
    for a in re.split(r"\s+and\s+", campo):
        sobrenome, _, prenome = (x.strip() for x in a.partition(","))
        exibido = f"{sobrenome}, {iniciais(prenome)}" if prenome else sobrenome
        ultimo = sem_acento(sobrenome.split()[-1]) if sobrenome else ""
        inicial = sem_acento(prenome[:1])
        ltfd = None
        for mid in membros:
            tokens = [sem_acento(t) for t in nomes_membros[mid].split() if t.lower() not in PARTICULAS]
            if ultimo in tokens and inicial == tokens[0][:1]:
                ltfd = mid
                break
        if ltfd:
            achados.add(ltfd)
        lista.append({"nome": exibido, "membro": ltfd})
    for mid in set(membros) - achados:
        avisos.append(f"{chave}: membro {mid} não encontrado entre os autores")
    return lista


def exportar(e: dict) -> str:
    """Entrada BibTeX limpa (sem os campos internos do LTFD), para download."""
    linhas = [f"@{e['tipo']}{{{e['chave']},"]
    linhas += [f"  {k} = {{{v}}}," for k, v in e["campos"].items() if k not in INTERNOS and v]
    linhas[-1] = linhas[-1].rstrip(",")
    return "\n".join(linhas + ["}"])


def main() -> None:
    raiz = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    nomes_membros = {}
    for arq in (raiz / "data" / "membros").glob("*.yaml"):
        nomes_membros[arq.stem] = yaml.safe_load(arq.read_text(encoding="utf-8"))["nome"]

    entradas = ler_bib((raiz / "bib" / "ltfd.bib").read_text(encoding="utf-8"))
    erros, avisos, saida = [], [], []
    chaves, dois = set(), set()
    for e in entradas:
        c, ch = e["campos"], e["chave"]
        for campo in OBRIGATORIOS:
            if not c.get(campo):
                erros.append(f"{ch}: falta o campo {campo}")
        if ch in chaves:
            erros.append(f"chave repetida: {ch}")
        chaves.add(ch)
        doi = c.get("doi", "").lower()
        if doi:
            if not re.fullmatch(r"10\.[0-9]{4,9}/\S+", doi):
                erros.append(f"{ch}: DOI fora do formato: {doi}")
            if doi in dois:
                erros.append(f"{ch}: DOI repetido: {doi}")
            dois.add(doi)
        if not c.get("year", "").isdigit():
            erros.append(f"{ch}: ano não numérico: {c.get('year')}")
            continue
        membros = [m.strip() for m in c.get("membros", "").split(",") if m.strip()]
        inexistentes = [m for m in membros if m not in nomes_membros]
        for m in inexistentes:
            erros.append(f"{ch}: membro inexistente: {m}")
        if inexistentes:
            continue
        saida.append({
            "chave": ch,
            "tipo": "artigo" if e["tipo"] == "article" else e["tipo"],
            "autores": autores(c.get("author", ""), membros, nomes_membros, ch, avisos),
            "titulo": c.get("title", "").replace("{", "").replace("}", ""),
            "veiculo": c.get("journal", ""),
            "volume": c.get("volume", ""),
            "numero": c.get("number", ""),
            "paginas": c.get("pages", "").replace("--", "–"),
            "ano": int(c["year"]),
            "doi": doi,
            "idioma": "en" if c.get("langid", "").lower() == "english" else "pt",
            "escopo": c.get("escopo", ""),
            "membros": membros,
            "bibtex": exportar(e),
        })

    saida.sort(key=lambda p: (-p["ano"], p["chave"]))
    for a in avisos:
        print("AVISO ", a)
    for e in erros:
        print("ERRO  ", e)
    if erros:
        sys.exit(1)
    destino = raiz / "data" / "gerado" / "publicacoes.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(saida, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    com_doi = sum(1 for p in saida if p["doi"])
    print(f"\n{len(saida)} publicações ({com_doi} com DOI) → {destino}: 0 erro(s), {len(avisos)} aviso(s).")


if __name__ == "__main__":
    main()
