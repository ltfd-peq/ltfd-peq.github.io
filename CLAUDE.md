# CLAUDE.md — site do LTFD

Site institucional do **LTFD – Laboratório de Termofluidodinâmica (PEQ/COPPE/UFRJ)**.
Gerador estático Hugo, tema próprio, dados em YAML, publicação no GitHub Pages
(`https://ltfd-peq.github.io/`). Idioma de trabalho: **pt-BR** (conteúdo, comentários,
mensagens de commit e de PR).

## Fontes de verdade (ler antes de mudar algo)

| O quê | Onde |
|---|---|
| Plano de implementação (arquitetura, páginas, dados, qualidade, cronograma) | `../3_Referencias_Sites/PLANO_IMPLEMENTACAO_SITE_LTFD.md` (v1.3) |
| Manual de identidade visual (prevalece sobre o plano em questões de marca) | `../2_logo_LTFD_2026/Manual_Uso/manual_marca_LTFD.pdf` e `.tex` |
| Logos oficiais 2026 | `../2_logo_LTFD_2026/Manual_Uso/logos/{svg,png,pdf,aplicacoes}/` |
| Kit de dados e artes (precisa de revisão; erros conhecidos no PLANO §7.4) | `../4_DataBase_Site_LTFD/` |
| Sites de referência analisados (só consulta; nunca copiar para cá) | `../3_Referencias_Sites/0X_*/` |
| Decisões tomadas neste repositório | `docs/decisoes/` |
| Andamento da campanha e próximos passos | `docs/CAMPANHA.md` |

As pastas `../` ficam no Dropbox, fora do repositório. O repositório é **público** e só
pode conter o que pode ir ao ar.

## Stack e versões fixas

- **Hugo 0.168.0, edição padrão** (sem *extended*). Atualização uma vez por semestre, num PR.
- Tema próprio em `layouts/` (sistema de templates da 0.146+: `layouts/_partials/`,
  `layouts/_shortcodes/`, `home.html`, `page.html`, `section.html`, `<secao>/page.html`).
- Sem frameworks CSS/JS, sem temas de terceiros, sem Node no build. JS só onde o PLANO §8
  prevê (hoje: `assets/js/menu.js`).
- APIs depreciadas que **não** usar: `site.Data` (use `hugo.Data`), `languageCode` (use
  `locale`), `languageName` (use `label`), `.Site.Sites`/`.Page.Sites` (use `hugo.Sites`),
  `.IsNode` (use `.IsBranch`), qualidade de imagem global (use `imaging.webp/avif.quality`).
  O CI usa `--panicOnWarning`: qualquer aviso derruba o build.
- Python 3.12 nos scripts, sempre com `python3 -I`. Dependências em `requirements.txt`.

## Marca (manual v1.0, out/2026)

- Fonte única: **Montserrat** (variável 400–800 + itálico 400), auto-hospedada em `static/fonts/`.
- Cores só pelos tokens de `assets/css/tokens.css`. Azul LTFD `#003366` domina; bordô
  `#8A2432` só em acentos (≈10 %). **Cor nova só depois de `scripts/contraste.py`.**
- Logo no header: versão **reduzida** (≥ 110 px de largura). Faixa institucional: **horizontal**
  (≥ 220 px). Fundo escuro: versão **branca**. Não pôr o emblema ao lado da marca principal.
  Nunca redigitar a sigla "LTFD" como logotipo; nunca distorcer, recolorir ou aplicar efeitos.
- Sem degradê decorativo (briefing de 2025). Cabeçalhos de página: faixa azul sólida.

## Dados (PLANO §7)

- Um YAML por registro: `data/linhas/<id>.yaml`, `data/membros/<id>.yaml`; `id` = nome do
  arquivo = slug da URL, e **nunca muda**. Páginas por registro vêm dos *content adapters*
  `content/pt/{pesquisa,equipe}/_content.gotmpl`.
- Guardar identificadores, não URLs (`ids.lattes`, `ids.orcid`…); o template monta o link.
- Todo registro tem `fonte`, `verificado_em` e `revisado_em`. **Fato sem fonte não vai ao ar.**
- Campos calculados nunca são digitados (membro atual × egresso, situação de projeto, vaga aberta).
- **Consentimento:** foto, e-mail de aluno e destino de egresso só entram no repositório com
  `consentimento.<campo>: true` (o `validar_dados.py` bloqueia). Termos assinados ficam no
  drive institucional, nunca aqui.
- Esquemas em `schemas/*.schema.json`; mudar um campo = mudar o esquema no mesmo PR.

## Qualidade (bloqueia o merge)

- WCAG 2.2 AA: 0 violações do axe; sem rolagem lateral a 320 px; menu operável pelo teclado.
- Orçamento: página inicial ≤ 500 KB e ≤ 25 requisições; internas ≤ 300 KB (`checar_peso.py`).
- `alt` em toda imagem (decorativa: `alt=""`); 1 H1 por página, sem saltos de nível.
- CSP em `<meta>` (`style-src 'self'`, `script-src 'self'`): **nada de `style="…"`, `<style>`
  ou `<script>` inline** (JSON-LD é permitido). SVG embutido usa atributos, não `<style>`.
- Nenhum "[a confirmar]", "a definir", "em construção" no build de produção.
- Endereço do site só no `baseURL` de `config/_default/hugo.toml`; templates usam
  `relURL`/`absURL`/`.Permalink`.

## Proibições

- Nenhum dado pessoal sem consentimento; nada que não possa ir ao ar.
- Nenhuma dependência nova sem justificativa no PR. Nenhum segredo em arquivo.
- Não copiar HTML, CSS, imagens ou textos dos sites de referência.
- Não inferir sobrenomes nem vínculos (ex.: lista de fotos de 2020: só primeiros nomes).
- Não mover o `.git` para dentro do Dropbox (ver `docs/decisoes/0003-repositorio-fora-do-dropbox.md`).

## Comandos

```bash
hugo server                                   # http://localhost:1313 (sem CSP, por causa do livereload)
python3 -I scripts/validar_dados.py           # esquemas, ids, referências, consentimentos
python3 -I scripts/contraste.py               # pares de cor (WCAG)
hugo build --environment provisorio --gc --minify --panicOnWarning
python3 -I scripts/checar_peso.py             # orçamento de peso sobre public/
python3 -I scripts/checar_marcadores.py --aviso
lychee --config tests/lychee.toml --offline --root-dir "$PWD/public" public
python3 -I tests/verificar_paginas.py --axe <caminho>/axe.min.js   # axe-core 4.13.0
```

Sem commits no repositório, o build `provisorio`/`producao` falha ao ler datas do Git; para
testar antes do primeiro commit: `HUGO_ENABLEGITINFO=false hugo build --environment provisorio`.

## Fluxo de cada mudança

1. Uma tarefa por *branch*; PR pequeno; o PR template lista a conferência.
2. Rodar os comandos acima e ver o resultado no navegador (desktop, 320 px, teclado).
3. CI verde antes do *merge*. O professor lê o *diff* e aprova.
4. Código legível para quem não usa o Claude Code: comentários curtos, sem abstrações desnecessárias.
