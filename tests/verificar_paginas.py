#!/usr/bin/env python3
"""Testes de navegador sobre o site gerado (public/): bloqueiam o merge no CI.

Uso:
    python3 -I tests/verificar_paginas.py --axe <axe.min.js> [--public public] [--capturas DIR]

Para cada página HTML de public/:
1. rolagem lateral a 320 px (scrollWidth <= clientWidth; WCAG 1.4.10, PLANO §4.3);
   nenhum erro no console (JavaScript ou violação da CSP);
2. axe-core com as regras WCAG 2.0/2.1/2.2 A e AA (inclui target-size), a 320 e a 1280 px:
   nenhuma violação é permitida (PLANO §10.1);
3. nenhum título (H1–H3) com palavra partida fora de um ponto de hifenização, de 320 a
   1920 px (o overflow-wrap corta em qualquer letra quando a palavra não cabe).
Na página inicial, também o menu móvel pelo teclado: Enter abre, Esc fecha e o foco
volta ao botão (C4). Com --capturas, grava telas de 390 e 1440 px de cada página.

O axe-core não fica no repositório: o CI instala a versão fixada com npm
(ver .github/workflows/pr.yml); localmente, baixe o pacote axe-core e aponte o arquivo.
"""
import argparse
import functools
import http.server
import socketserver
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

TAGS_WCAG = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22a", "wcag22aa"]


def servir(pasta: Path) -> tuple[socketserver.TCPServer, str]:
    class Silencioso(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    handler = functools.partial(Silencioso, directory=str(pasta))
    servidor = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor, f"http://127.0.0.1:{servidor.server_address[1]}"


def paginas(pasta: Path) -> list[str]:
    caminhos = []
    for html in sorted(pasta.rglob("*.html")):
        rel = html.relative_to(pasta).as_posix()
        caminhos.append("/" + rel.removesuffix("index.html"))
    return caminhos


LARGURAS_TITULOS = (320, 390, 768, 1024, 1280, 1440, 1920)

# Acha palavras de títulos quebradas no meio, fora de um ponto de hifenização: o
# overflow-wrap corta em qualquer letra quando a palavra não cabe (ex.: "Termofluidodinâmic|a").
# Mede a posição de cada letra; mudança de linha dentro de uma palavra só é aceita logo
# depois de um &shy; (U+00AD) ou de um hífen.
JS_PALAVRAS_PARTIDAS = """() => {
  const achados = [];
  for (const titulo of document.querySelectorAll('h1, h2, h3')) {
    const passos = document.createTreeWalker(titulo, NodeFilter.SHOW_TEXT);
    for (let no = passos.nextNode(); no; no = passos.nextNode()) {
      const t = no.textContent, faixa = document.createRange();
      let topoAnterior = null;
      for (let i = 0; i < t.length; i++) {
        if (/\\s/.test(t[i])) { topoAnterior = null; continue; }
        faixa.setStart(no, i); faixa.setEnd(no, i + 1);
        // logo após uma quebra o Chromium devolve 2 retângulos (o 1º na linha anterior): vale o último
        const rs = faixa.getClientRects(), r = rs[rs.length - 1];
        if (!r || r.width === 0) continue;
        if (topoAnterior !== null && r.top - topoAnterior > 2 && !['\\u00AD', '-', '‐'].includes(t[i - 1])) {
          const ini = t.lastIndexOf(' ', i) + 1, fim = t.indexOf(' ', i);
          achados.push(`"${t.slice(ini, fim < 0 ? t.length : fim).replace(/\\u00AD/g, '')}" partida antes de "${t[i]}"`);
        }
        topoAnterior = r.top;
      }
    }
  }
  return achados;
}"""


def rodar_axe(pagina, axe_js: str) -> list[dict]:
    pagina.add_script_tag(content=axe_js)
    return pagina.evaluate(
        """async (tags) => {
            const r = await axe.run(document, {runOnly: {type: 'tag', values: tags}, resultTypes: ['violations']});
            return r.violations.map(v => ({id: v.id, impacto: v.impact, ajuda: v.help,
                                           alvos: v.nodes.slice(0, 5).map(n => n.target.join(' '))}));
        }""",
        TAGS_WCAG,
    )


def testar_menu(navegador, base: str) -> list[str]:
    erros = []
    contexto = navegador.new_context(viewport={"width": 390, "height": 844})
    p = contexto.new_page()
    p.goto(base + "/")
    botao = p.locator(".nav__botao")
    if not botao.is_visible():
        return ["menu: o botão 'Menu' não aparece a 390 px"]
    botao.focus()
    p.keyboard.press("Enter")
    if botao.get_attribute("aria-expanded") != "true" or not p.locator("#nav-painel").is_visible():
        erros.append("menu: Enter não abriu o painel (aria-expanded/visibilidade)")
    p.keyboard.press("Escape")
    if botao.get_attribute("aria-expanded") != "false":
        erros.append("menu: Esc não fechou o painel")
    if not p.evaluate("document.activeElement === document.querySelector('.nav__botao')"):
        erros.append("menu: o foco não voltou ao botão depois do Esc")
    contexto.close()
    return erros


def main() -> None:
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--public", default="public")
    args.add_argument("--axe", required=True, help="caminho do axe.min.js")
    args.add_argument("--capturas", help="pasta para gravar capturas de tela")
    opcoes = args.parse_args()

    pasta = Path(opcoes.public)
    axe_js = Path(opcoes.axe).read_text(encoding="utf-8")
    servidor, base = servir(pasta)
    falhas = []
    with sync_playwright() as pw:
        navegador = pw.chromium.launch()

        # 1) Com a CSP valendo: nenhum erro de JavaScript nem violação da CSP no console.
        contexto = navegador.new_context(viewport={"width": 1280, "height": 900}, locale="pt-BR")
        p = contexto.new_page()
        erros_console = []
        p.on("console", lambda msg: erros_console.append(msg.text) if msg.type == "error" else None)
        p.on("pageerror", lambda exc: erros_console.append(str(exc)))
        for caminho in paginas(pasta):
            erros_console.clear()
            p.goto(base + caminho)
            falhas += [f"{caminho}: erro no console: {e}" for e in erros_console]
        contexto.close()

        # 2) Títulos sem palavra partida, em várias larguras (a fonte dos títulos é fluida).
        for largura in LARGURAS_TITULOS:
            contexto = navegador.new_context(viewport={"width": largura, "height": 900}, locale="pt-BR")
            p = contexto.new_page()
            for caminho in paginas(pasta):
                p.goto(base + caminho)
                p.evaluate("document.fonts.ready.then(() => true)")  # medir com a Montserrat carregada
                falhas += [f"{caminho} @{largura}px: título com {a}" for a in p.evaluate(JS_PALAVRAS_PARTIDAS)]
            contexto.close()

        # 3) Rolagem lateral e axe. bypass_csp: o axe é injetado como script inline,
        #    que a CSP do site (corretamente) bloqueia.
        for largura in (320, 1280):
            contexto = navegador.new_context(viewport={"width": largura, "height": 900}, locale="pt-BR", bypass_csp=True)
            p = contexto.new_page()
            for caminho in paginas(pasta):
                p.goto(base + caminho)
                if largura == 320:
                    excesso = p.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                    if excesso > 0:
                        falhas.append(f"{caminho}: rolagem lateral de {excesso} px a 320 px")
                for v in rodar_axe(p, axe_js):
                    falhas.append(f"{caminho} @{largura}px: [{v['impacto']}] {v['id']} – {v['ajuda']} → {v['alvos']}")
            contexto.close()
        falhas += testar_menu(navegador, base)

        if opcoes.capturas:
            destino = Path(opcoes.capturas)
            destino.mkdir(parents=True, exist_ok=True)
            for largura in (390, 1440):
                contexto = navegador.new_context(viewport={"width": largura, "height": 900}, device_scale_factor=1)
                p = contexto.new_page()
                for caminho in paginas(pasta):
                    p.goto(base + caminho)
                    # a captura pode sair antes de a imagem (AVIF) ser decodificada e pintada
                    p.evaluate("Promise.all(Array.from(document.images).map(i => i.decode().catch(() => null)))")
                    nome = (caminho.strip("/").replace("/", "_") or "inicio").removesuffix(".html")
                    p.screenshot(path=str(destino / f"{nome}-{largura}.png"), full_page=True)
                contexto.close()
        navegador.close()
    servidor.shutdown()

    for f in falhas:
        print("FALHA ", f)
    total = len(paginas(pasta))
    if falhas:
        sys.exit(f"\n{len(falhas)} falha(s) em {total} páginas.")
    print(f"{total} páginas: sem rolagem lateral a 320 px, 0 violações do axe (WCAG 2.2 AA), menu ok.")


if __name__ == "__main__":
    main()
