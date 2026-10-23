#!/usr/bin/env python3
"""Valida os dados do site (data/) antes do build. Bloqueia o merge no CI.

Uso:
    python3 -I scripts/validar_dados.py [raiz_do_repositorio]

Erros (saída com código 1):
- esquema JSON de cada coleção (schemas/*.schema.json);
- id diferente do nome do arquivo;
- referência a linha ou membro inexistente; docente responsável que não é docente;
- dígito verificador do ORCID;
- regra do repositório público (PLANO §7.1, princípio 9): e-mail de quem não é docente,
  foto ou destino sem o consentimento correspondente.
Avisos (relatório, não bloqueiam; metas do PLANO §4.3):
- membro atual sem Lattes; docente, pós-doc ou doutorando sem ORCID;
- aluno sem título de trabalho ou sem linha.
"""
import datetime as dt
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

CATEGORIAS_ORCID = {"docente", "pesquisador", "pos-doutorado", "doutorado"}


def carregar_yaml(caminho: Path):
    def normalizar(x):
        if isinstance(x, (dt.date, dt.datetime)):
            return x.isoformat()[:10]
        if isinstance(x, dict):
            return {k: normalizar(v) for k, v in x.items()}
        if isinstance(x, list):
            return [normalizar(v) for v in x]
        return x
    return normalizar(yaml.safe_load(caminho.read_text(encoding="utf-8")))


def orcid_valido(orcid: str) -> bool:
    """Dígito verificador ISO 7064 MOD 11-2."""
    digitos = orcid.replace("-", "")
    total = 0
    for c in digitos[:-1]:
        total = (total + int(c)) * 2
    resto = (12 - total % 11) % 11
    return digitos[-1] == ("X" if resto == 10 else str(resto))


def main() -> None:
    raiz = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    esquemas = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in (raiz / "schemas").glob("*.schema.json")}
    registro = Registry().with_resources((nome, Resource.from_contents(e)) for nome, e in esquemas.items())

    def validador(nome):
        return Draft202012Validator(esquemas[nome], registry=registro, format_checker=FormatChecker())

    erros, avisos = [], []

    def validar(caminho: Path, dados, esquema: str):
        for e in sorted(validador(esquema).iter_errors(dados), key=lambda e: list(e.path)):
            local = "/".join(str(p) for p in e.path) or "(raiz)"
            erros.append(f"{caminho}: {local}: {e.message}")

    dados = raiz / "data"
    lab = carregar_yaml(dados / "laboratorio.yaml")
    validar(dados / "laboratorio.yaml", lab, "laboratorio.schema.json")
    hist = carregar_yaml(dados / "historico.yaml")
    validar(dados / "historico.yaml", hist, "historico.schema.json")

    colecoes = {}
    for colecao, esquema in (("linhas", "linha.schema.json"), ("membros", "membro.schema.json")):
        colecoes[colecao] = {}
        for arq in sorted((dados / colecao).glob("*.yaml")):
            reg = carregar_yaml(arq)
            validar(arq, reg, esquema)
            if reg.get("id") != arq.stem:
                erros.append(f"{arq}: id '{reg.get('id')}' diferente do nome do arquivo '{arq.stem}'")
            colecoes[colecao][arq.stem] = reg

    linhas, membros = colecoes["linhas"], colecoes["membros"]
    ordens = [l.get("ordem") for l in linhas.values()]
    if len(ordens) != len(set(ordens)):
        erros.append("data/linhas: há linhas com a mesma 'ordem'")

    for lid, l in linhas.items():
        for d in l.get("docentes_responsaveis", []):
            if d not in membros:
                erros.append(f"data/linhas/{lid}.yaml: docente responsável inexistente: {d}")
            elif membros[d].get("categoria") != "docente":
                erros.append(f"data/linhas/{lid}.yaml: {d} não é docente")
        if not (raiz / "assets" / "icones" / f"{l.get('icone')}.svg").exists():
            erros.append(f"data/linhas/{lid}.yaml: ícone inexistente: assets/icones/{l.get('icone')}.svg")

    for mid, m in membros.items():
        arq = f"data/membros/{mid}.yaml"
        cat = m.get("categoria")
        atual = not (m.get("periodo") or {}).get("fim")
        consent = m.get("consentimento") or {}
        for l in m.get("linhas", []):
            if l not in linhas:
                erros.append(f"{arq}: linha inexistente: {l}")
        trabalho = m.get("trabalho") or {}
        for papel in ("orientadores", "coorientadores"):
            for p in trabalho.get(papel, []):
                if isinstance(p, str) and p not in membros:
                    erros.append(f"{arq}: {papel}: membro inexistente: {p} (pessoa externa: use {{nome, instituicao}})")
        orcid = (m.get("ids") or {}).get("orcid")
        if orcid and not orcid_valido(orcid):
            erros.append(f"{arq}: ORCID com dígito verificador inválido: {orcid}")
        # Repositório público: só o que pode ir ao ar (PLANO §7.1, princípio 9; §10.4)
        if m.get("email") and cat != "docente" and consent.get("email") is not True:
            erros.append(f"{arq}: e-mail sem consentimento.email: true")
        if m.get("foto") and consent.get("foto") is not True:
            erros.append(f"{arq}: foto sem consentimento.foto: true")
        if m.get("destino") and consent.get("destino") is not True:
            erros.append(f"{arq}: destino sem consentimento.destino: true")
        if m.get("foto") and not (raiz / "assets" / "img" / "equipe" / m["foto"]).exists():
            erros.append(f"{arq}: arquivo de foto inexistente: assets/img/equipe/{m['foto']}")
        # Relatório (metas semestrais)
        if atual and not (m.get("ids") or {}).get("lattes") and cat != "colaborador-externo":
            avisos.append(f"{arq}: membro atual sem Lattes")
        if atual and cat in CATEGORIAS_ORCID and not orcid:
            avisos.append(f"{arq}: {cat} sem ORCID")
        if cat != "docente" and atual and not trabalho.get("titulo"):
            avisos.append(f"{arq}: sem título do trabalho")
        if atual and not m.get("linhas"):
            avisos.append(f"{arq}: sem linha de pesquisa")

    for a in avisos:
        print("AVISO ", a)
    for e in erros:
        print("ERRO  ", e)
    print(f"\n{len(linhas)} linhas e {len(membros)} membros conferidos: {len(erros)} erro(s), {len(avisos)} aviso(s).")
    if erros:
        sys.exit(1)


if __name__ == "__main__":
    main()
