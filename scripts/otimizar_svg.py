#!/usr/bin/env python3
"""Reduz o peso dos SVGs de marca sem alterar o desenho.

Uso:
    python3 -I scripts/otimizar_svg.py <entrada.svg> <saida.svg> [casas_decimais]

O que faz:
- arredonda as coordenadas dos caminhos (padrão: 1 casa; os viewBox dos logos
  têm milhares de unidades, então 0,1 unidade some na tela);
- converte style="fill:…" em atributos fill="…" (a CSP do site, style-src 'self',
  bloqueia atributos style quando o SVG é embutido no HTML);
- remove metadados e atributos do Inkscape/Sodipodi, ids e comentários.

Confira o resultado com scripts/comparar_svg.py antes de publicar.
"""
import re
import sys
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
NUMERO = re.compile(r"-?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")
ESTILOS_UTEIS = {"fill", "fill-rule", "fill-opacity", "stroke", "stroke-width", "opacity", "clip-rule"}


def arredondar(texto: str, casas: int) -> str:
    def troca(m: re.Match) -> str:
        valor = round(float(m.group(0)), casas)
        s = f"{valor:.{casas}f}".rstrip("0").rstrip(".") if casas else str(int(valor))
        return "0" if s in ("-0", "") else s
    return NUMERO.sub(troca, texto)


def ids_referenciados(raiz: ET.Element) -> set[str]:
    """ids usados em url(#…) ou href="#…" (clipPath, gradientes): não podem sair."""
    usados = set()
    for elem in raiz.iter():
        for valor in elem.attrib.values():
            usados.update(re.findall(r"url\(#([^)]+)\)", valor))
            if valor.startswith("#"):
                usados.add(valor[1:])
    return usados


def limpar(elem: ET.Element, casas: int, manter: set[str]) -> None:
    for chave in list(elem.attrib):
        local = chave.split("}")[-1]
        if chave.startswith("{") and not chave.startswith("{" + SVG_NS) and local != "href":
            del elem.attrib[chave]            # inkscape:*, sodipodi:*
        elif local == "id" and elem.attrib[chave] not in manter:
            del elem.attrib[chave]
    estilo = elem.attrib.pop("style", "")
    for decl in filter(None, (d.strip() for d in estilo.split(";"))):
        prop, _, valor = decl.partition(":")
        prop = prop.strip()
        # stroke-width sem stroke não desenha nada: só ocupa bytes
        if prop in ESTILOS_UTEIS and not (prop == "stroke-width" and "stroke" not in estilo.replace("stroke-width", "")):
            elem.set(prop, valor.strip())
    if "d" in elem.attrib:
        elem.set("d", arredondar(elem.attrib["d"], casas))
    if "transform" in elem.attrib:
        elem.set("transform", arredondar(elem.attrib["transform"], 6))
    for filho in list(elem):
        tag = filho.tag.split("}")[-1]
        if not filho.tag.startswith("{" + SVG_NS) or tag in ("metadata", "defs") and len(filho) == 0:
            elem.remove(filho)
            continue
        limpar(filho, casas, manter)


def main() -> None:
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    casas = int(sys.argv[3]) if len(sys.argv) == 4 else 1
    arvore = ET.parse(sys.argv[1])
    raiz = arvore.getroot()
    limpar(raiz, casas, ids_referenciados(raiz))
    for elem in raiz.iter():
        if elem.text and not elem.text.strip():
            elem.text = None
        elem.tail = None
    arvore.write(sys.argv[2], encoding="utf-8", xml_declaration=False)


if __name__ == "__main__":
    main()
