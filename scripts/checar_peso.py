#!/usr/bin/env python3
"""Orçamento de peso das páginas (PLANO §10.2), calculado sobre public/. Determinístico.

Uso:
    python3 -I scripts/checar_peso.py [public]

Para cada página: HTML + CSS + JS + fontes + imagens + favicon que um celular
(390 px, DPR 2) baixa ao abrir a página com o cache vazio. Texto (HTML, CSS, JS,
SVG) conta com gzip -9, como o servidor entrega; binários contam o tamanho bruto.
Imagens com loading="lazy" entram na conta (são poucas e pequenas): a estimativa
fica do lado conservador. Fontes: o arquivo latin normal sempre; o itálico só se a
página tiver <em>, <i> ou <cite>.
Metas: página inicial ≤ 500 KB e ≤ 25 requisições; Equipe ≤ 600 KB; demais ≤ 300 KB.
"""
import gzip
import re
import sys
from pathlib import Path

KB = 1024
METAS = {"/": (500 * KB, 25), "/equipe/": (600 * KB, 40)}
META_PADRAO = (300 * KB, 25)
TEXTO = {".html", ".css", ".js", ".svg", ".json", ".xml", ".txt"}


def bytes_entregues(arq: Path) -> int:
    dados = arq.read_bytes()
    return len(gzip.compress(dados, 9)) if arq.suffix in TEXTO else len(dados)


def escolher_srcset(srcset: str, alvo: int = 780) -> str:
    """Candidato que o navegador escolheria para 390 px × DPR 2 (largura ≥ 780)."""
    cands = []
    for parte in srcset.split(","):
        url, _, desc = parte.strip().partition(" ")
        cands.append((int(desc.rstrip("w")) if desc.endswith("w") else 0, url))
    cands.sort()
    for largura, url in cands:
        if largura >= alvo:
            return url
    return cands[-1][1]


def recursos(html: str) -> set[str]:
    urls = set()
    urls.update(re.findall(r'<link[^>]+rel="?stylesheet"?[^>]+href="?([^" >]+)', html))
    urls.update(re.findall(r'<script[^>]+src="?([^" >]+)', html))
    urls.update(re.findall(r'<link[^>]+rel="?icon"?[^>]+href="?([^" >]+\.svg)', html))
    for pic in re.findall(r"<picture.*?</picture>", html, flags=re.S):
        # celular: a última <source> sem media, preferindo AVIF (o primeiro tipo listado)
        fontes = [s for s in re.findall(r"<source([^>]+)>", pic) if "media=" not in s]
        if fontes:
            srcset = re.search(r'srcset="?([^"]+)"', fontes[0]).group(1)
            urls.add(escolher_srcset(srcset))
    sem_picture = re.sub(r"<picture.*?</picture>", "", html, flags=re.S)
    urls.update(re.findall(r'<img[^>]+src="?([^" >]+)', sem_picture))
    urls.add("/fonts/montserrat-var-latin.woff2")
    if re.search(r"<(em|i|cite)\b", html):
        urls.add("/fonts/montserrat-italic-400-latin.woff2")
    return {u for u in urls if u.startswith("/") and not u.startswith("//")}


def main() -> None:
    public = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
    falhas = 0
    for html_arq in sorted(public.rglob("index.html")):
        caminho = "/" + html_arq.parent.relative_to(public).as_posix().strip(".") + "/"
        caminho = caminho.replace("//", "/")
        html = html_arq.read_text(encoding="utf-8")
        total, n = bytes_entregues(html_arq), 1
        for url in sorted(recursos(html)):
            arq = public / url.lstrip("/").split("?")[0]
            if not arq.exists():
                print(f"ERRO   {caminho}: recurso inexistente {url}")
                falhas += 1
                continue
            total += bytes_entregues(arq)
            n += 1
        meta_bytes, meta_req = METAS.get(caminho, META_PADRAO)
        ok = total <= meta_bytes and n <= meta_req
        falhas += not ok
        print(f"{'ok ' if ok else 'FALHA'}  {total / KB:6.1f} KB em {n:2d} requisições (meta {meta_bytes // KB} KB, {meta_req})  {caminho}")
    if falhas:
        sys.exit(f"\n{falhas} página(s) fora do orçamento.")


if __name__ == "__main__":
    main()
