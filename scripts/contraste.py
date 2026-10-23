#!/usr/bin/env python3
"""Verifica o contraste (WCAG 2.x) de todos os pares de cor usados no tema.

Uso:
    python3 -I scripts/contraste.py [assets/css/tokens.css]

Lê os valores das primitivas (--ltfd-*) e de alguns semânticos direto do
tokens.css, para que o teste acompanhe qualquer mudança de cor. Cor nova no
tema = par novo aqui (PLANO §8.2). Sai com erro se algum par ficar abaixo do
mínimo: 4,5:1 para texto, 3:1 para bordas, foco e indicadores (1.4.11).
"""
import re
import sys
from pathlib import Path

TEXTO, NAO_TEXTO = 4.5, 3.0

# (frente, fundo, mínimo, onde aparece). Nomes sem o prefixo "--".
# "veu-sobre-branco" é a cor composta do véu do hero sobre o pior pixel da imagem.
PARES = [
    ("ltfd-preto-90", "ltfd-branco", TEXTO, "texto corrido"),
    ("ltfd-preto-90", "ltfd-fundo", TEXTO, "texto em seção alternada"),
    ("ltfd-preto-90", "ltfd-azul-gelo", TEXTO, "texto em caixa de destaque"),
    ("ltfd-ardosia", "ltfd-branco", TEXTO, "texto secundário"),
    ("ltfd-ardosia", "ltfd-fundo", TEXTO, "texto secundário em seção alternada"),
    ("ltfd-ardosia", "ltfd-azul-gelo", TEXTO, "texto secundário em caixa de destaque"),
    ("ltfd-azul", "ltfd-branco", TEXTO, "títulos"),
    ("ltfd-azul", "ltfd-fundo", TEXTO, "títulos em seção alternada"),
    ("ltfd-azul", "ltfd-azul-gelo", TEXTO, "chips e títulos em destaque"),
    ("ltfd-bordo", "ltfd-branco", TEXTO, "sobretítulos"),
    ("ltfd-bordo", "ltfd-fundo", TEXTO, "sobretítulos em seção alternada"),
    ("ltfd-bordo", "ltfd-bordo-gelo", TEXTO, "selos de tipo"),
    ("ltfd-azul-medio", "ltfd-branco", TEXTO, "links"),
    ("ltfd-azul-medio", "ltfd-fundo", TEXTO, "links em seção alternada"),
    ("ltfd-azul-medio", "ltfd-azul-gelo", TEXTO, "links em caixa de destaque"),
    ("ltfd-verde", "ltfd-verde-gelo", TEXTO, "selo 'Em andamento'"),
    ("ltfd-branco", "ltfd-azul", TEXTO, "texto em faixa azul e botão"),
    ("ltfd-branco", "ltfd-azul-profundo", TEXTO, "rodapé e botão em hover"),
    ("ltfd-branco", "ltfd-bordo", TEXTO, "botão de destaque"),
    ("ltfd-branco", "cor-botao2-fundo-hover", TEXTO, "botão de destaque em hover"),
    ("ltfd-branco", "veu-sobre-branco", TEXTO, "texto do hero sobre o véu"),
    ("ltfd-rodape-texto-2", "ltfd-azul-profundo", TEXTO, "texto secundário do rodapé"),
    ("ltfd-rodape-texto-2", "ltfd-azul", TEXTO, "texto secundário em faixa azul"),
    ("ltfd-azul-claro", "ltfd-azul-profundo", TEXTO, "links do rodapé"),
    ("ltfd-azul-claro", "ltfd-azul", TEXTO, "links em faixa azul"),
    ("ltfd-azul", "ltfd-branco", NAO_TEXTO, "anel de foco"),
    ("ltfd-azul", "ltfd-fundo", NAO_TEXTO, "anel de foco em seção alternada"),
    ("ltfd-ambar-foco", "ltfd-azul", NAO_TEXTO, "anel de foco em faixa azul"),
    ("ltfd-ambar-foco", "ltfd-azul-profundo", NAO_TEXTO, "anel de foco no rodapé"),
    ("ltfd-ambar-foco", "veu-sobre-branco", NAO_TEXTO, "anel de foco no hero"),
    ("ltfd-cinza-controle", "ltfd-branco", NAO_TEXTO, "borda de campo"),
    ("ltfd-cinza-controle", "ltfd-fundo", NAO_TEXTO, "borda de campo em seção alternada"),
    ("ltfd-bordo", "ltfd-branco", NAO_TEXTO, "filete do item de menu ativo"),
]


def hex_rgb(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def luminancia(rgb) -> float:
    def canal(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def razao(a, b) -> float:
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def ler_cores(css: str) -> dict:
    cores = {m.group(1): hex_rgb(m.group(2))
             for m in re.finditer(r"--([\w-]+):\s*(#[0-9A-Fa-f]{6})\b", css)}
    veu = re.search(r"--cor-veu-hero:\s*rgb\((\d+) (\d+) (\d+) / ([\d.]+)\)", css)
    if veu:
        r, g, b, alfa = (float(x) for x in veu.groups())
        cores["veu-sobre-branco"] = tuple(alfa * c / 255 + (1 - alfa) for c in (r, g, b))
    return cores


def main() -> None:
    arquivo = Path(sys.argv[1] if len(sys.argv) > 1 else "assets/css/tokens.css")
    cores = ler_cores(arquivo.read_text(encoding="utf-8"))
    falhas = 0
    for frente, fundo, minimo, onde in PARES:
        if frente not in cores or fundo not in cores:
            print(f"ERRO   cor ausente em {arquivo}: {frente if frente not in cores else fundo}")
            falhas += 1
            continue
        r = razao(cores[frente], cores[fundo])
        ok = r >= minimo
        falhas += not ok
        print(f"{'ok ' if ok else 'FALHA'}  {r:5.2f}:1 (mín. {minimo})  {frente} sobre {fundo} — {onde}")
    if falhas:
        sys.exit(f"\n{falhas} par(es) abaixo do mínimo.")
    print(f"\n{len(PARES)} pares conferidos.")


if __name__ == "__main__":
    main()
