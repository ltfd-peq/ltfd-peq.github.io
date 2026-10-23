#!/usr/bin/env python3
"""Compara dois SVGs rasterizados (Inkscape) e falha se o desenho mudou.

Uso:
    python3 -I scripts/comparar_svg.py <original.svg> <otimizado.svg> [largura_px]

Rasteriza os dois na mesma largura (padrão: 1200 px) e conta os pixels cuja
cor difere em mais de 32 níveis em algum canal. Aceita até 0,1 % de pixels
diferentes (bordas suavizadas).
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops


def rasterizar(svg: str, largura: int, destino: Path) -> Image.Image:
    subprocess.run(
        ["inkscape", svg, "--export-type=png", f"--export-filename={destino}",
         f"--export-width={largura}", "--export-background-opacity=0"],
        check=True, capture_output=True,
    )
    return Image.open(destino).convert("RGBA")


def main() -> None:
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    largura = int(sys.argv[3]) if len(sys.argv) == 4 else 1200
    with tempfile.TemporaryDirectory() as tmp:
        a = rasterizar(sys.argv[1], largura, Path(tmp) / "a.png")
        b = rasterizar(sys.argv[2], largura, Path(tmp) / "b.png")
    if a.size != b.size:
        sys.exit(f"Tamanhos diferentes: {a.size} × {b.size}")
    dif = ImageChops.difference(a, b)
    diferentes = sum(1 for px in dif.getdata() if max(px) > 32)
    total = a.size[0] * a.size[1]
    fracao = diferentes / total
    print(f"{Path(sys.argv[2]).name}: {diferentes} de {total} pixels diferentes ({fracao:.4%})")
    if fracao > 0.001:
        sys.exit(1)


if __name__ == "__main__":
    main()
