#!/usr/bin/env python3
"""Gera a imagem Open Graph do site (1200×630 px).

Uso:
    python3 -I scripts/gerar_og.py <ltfd-vertical-branca.svg> static/img/og-ltfd.png

Composição como a capa do Manual de Identidade Visual: fundo Azul LTFD (#003366),
faixa Bordô LTFD (#8A2432) na base e a marca vertical na versão negativa (branca),
centralizada, com folga maior que a área de proteção. Requer Inkscape e Pillow.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

LARGURA, ALTURA, FAIXA = 1200, 630, 28
AZUL, BORDO = (0, 51, 102), (138, 36, 50)


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    svg, saida = Path(sys.argv[1]), Path(sys.argv[2])
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "logo.png"
        subprocess.run(["inkscape", str(svg), "--export-type=png", f"--export-filename={png}",
                        "--export-height=400", "--export-background-opacity=0"],
                       check=True, capture_output=True)
        logo = Image.open(png).convert("RGBA")
    tela = Image.new("RGBA", (LARGURA, ALTURA), AZUL + (255,))
    tela.paste(Image.new("RGBA", (LARGURA, FAIXA), BORDO + (255,)), (0, ALTURA - FAIXA))
    util = ALTURA - FAIXA
    tela.alpha_composite(logo, ((LARGURA - logo.width) // 2, (util - logo.height) // 2))
    saida.parent.mkdir(parents=True, exist_ok=True)
    tela.convert("RGB").save(saida, optimize=True)
    print(saida, saida.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
