#!/usr/bin/env python3
"""Gera favicon.ico, apple-touch-icon.png e ícones 192/512 quadrados.

Uso:
    python3 -I scripts/gerar_icones.py <ltfd-simbolo-colorida.svg> static

Por quê: os PNG/ICO de 0_Site_LTFD/2_logo_LTFD_2026/Manual_Uso/logos/aplicacoes/
seguem a proporção do símbolo (1:1,04) e saem com 16×17, 32×33 e 180×187 px.
Navegadores e o iOS esperam ícones quadrados; aqui o símbolo é centralizado
num quadrado, com margem, sem deformar (manual, seção "Usos incorretos").
- favicon.ico (16, 32, 48): fundo transparente, margem mínima;
- apple-touch-icon.png (180) e img/icone-{192,512}.png: fundo branco opaco
  (o iOS pinta de preto o que for transparente) e margem de 12 %.
Requer Inkscape e Pillow.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


def rasterizar(svg: Path, altura: int, destino: Path) -> Image.Image:
    subprocess.run(
        ["inkscape", str(svg), "--export-type=png", f"--export-filename={destino}",
         f"--export-height={altura}", "--export-background-opacity=0"],
        check=True, capture_output=True,
    )
    return Image.open(destino).convert("RGBA")


def quadrado(svg: Path, lado: int, margem: float, fundo, tmp: Path) -> Image.Image:
    util = round(lado * (1 - 2 * margem))
    simbolo = rasterizar(svg, util, tmp / f"s{lado}.png")
    if simbolo.width > util:  # o símbolo é um pouco mais largo que alto
        simbolo = simbolo.resize((util, round(simbolo.height * util / simbolo.width)), Image.LANCZOS)
    tela = Image.new("RGBA", (lado, lado), fundo)
    tela.alpha_composite(simbolo, ((lado - simbolo.width) // 2, (lado - simbolo.height) // 2))
    return tela


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    svg, saida = Path(sys.argv[1]), Path(sys.argv[2])
    (saida / "img").mkdir(parents=True, exist_ok=True)
    branco = (255, 255, 255, 255)
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        icones = [quadrado(svg, lado, 0.02, (0, 0, 0, 0), tmp) for lado in (16, 32, 48)]
        icones[-1].save(saida / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)],
                        append_images=icones[:-1])
        quadrado(svg, 180, 0.12, branco, tmp).convert("RGB").save(saida / "apple-touch-icon.png", optimize=True)
        for lado in (192, 512):
            quadrado(svg, lado, 0.12, branco, tmp).convert("RGB").save(saida / "img" / f"icone-{lado}.png", optimize=True)
    for f in ["favicon.ico", "apple-touch-icon.png", "img/icone-192.png", "img/icone-512.png"]:
        print(f, (saida / f).stat().st_size, "bytes")


if __name__ == "__main__":
    main()
