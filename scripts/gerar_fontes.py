#!/usr/bin/env python3
"""Gera as fontes web (woff2) do site a partir dos arquivos da marca.

Uso:
    python3 -I scripts/gerar_fontes.py <Montserrat[wght].ttf> <Montserrat-Italic.otf> static/fonts

Fontes de origem (licença OFL):
- Montserrat variável: 0_Site_LTFD/4_DataBase_Site_LTFD/artes/fontes/Montserrat[wght].ttf
- Montserrat itálico:  0_Site_LTFD/2_logo_LTFD_2026/Manual_Uso/fontes/Montserrat-Italic.otf

Cada estilo é dividido em dois arquivos (latin e latin-ext), com os mesmos
intervalos que o Google Fonts usa; o navegador só baixa o latin-ext se a
página tiver algum caractere dele. O eixo de peso da variável é limitado a
400–800, os pesos que o tema usa (assets/css/tokens.css).
"""
import io
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

LATIN = (
    "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,"
    "U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
)
LATIN_EXT = (
    "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,"
    "U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C4,"
    "U+2113,U+2C60-2C7F,U+A720-A7FF"
)
FAIXAS = {"latin": LATIN, "latin-ext": LATIN_EXT}


def unicodes(faixa: str) -> list[int]:
    saida = []
    for parte in faixa.split(","):
        parte = parte.strip().removeprefix("U+")
        if "-" in parte:
            ini, fim = parte.split("-")
            saida.extend(range(int(ini, 16), int(fim, 16) + 1))
        else:
            saida.append(int(parte, 16))
    return saida


def gravar_subconjunto(fonte: TTFont, faixa: str, destino: Path) -> None:
    opcoes = subset.Options()
    opcoes.flavor = "woff2"
    opcoes.layout_features += ["tnum", "lnum", "case"]  # padrão (kern, liga…) + numerais tabulares
    opcoes.name_IDs = ["*"]
    opcoes.notdef_outline = True
    opcoes.hinting = False              # telas modernas não precisam; reduz o arquivo
    sub = subset.Subsetter(opcoes)
    sub.populate(unicodes=unicodes(faixa))
    sub.subset(fonte)  # altera a fonte no lugar: o chamador passa sempre uma cópia nova
    fonte.flavor = "woff2"
    fonte.save(destino)
    print(f"{destino}  {destino.stat().st_size / 1024:.1f} KB")


def main() -> None:
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    variavel, italico, saida = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    saida.mkdir(parents=True, exist_ok=True)

    # Limita o eixo e recarrega a fonte: sem a volta por bytes, o subconjunto
    # falha no gvar com algumas versões do fontTools (KeyError em glifos de espaço).
    buffer = io.BytesIO()
    instancer.instantiateVariableFont(TTFont(variavel), {"wght": (400, 800)}).save(buffer)

    for nome, faixa in FAIXAS.items():
        buffer.seek(0)
        gravar_subconjunto(TTFont(buffer), faixa, saida / f"montserrat-var-{nome}.woff2")

        gravar_subconjunto(TTFont(italico), faixa, saida / f"montserrat-italic-400-{nome}.woff2")


if __name__ == "__main__":
    main()
