# Site do LTFD — Laboratório de Termofluidodinâmica (PEQ/COPPE/UFRJ)

Código e conteúdo do site do LTFD, publicado em **https://ltfd-peq.github.io/**.
Site estático gerado pelo [Hugo](https://gohugo.io/) a partir de arquivos de dados (YAML) e
textos (Markdown), publicado pelo GitHub Actions no GitHub Pages. Não há banco de dados nem
código rodando no servidor.

## Rodar no seu computador (3 comandos)

Requisitos: [Hugo 0.168.0](https://github.com/gohugoio/hugo/releases/tag/v0.168.0)
(edição padrão) e Git. Para os testes, Python 3.12.

```bash
git clone https://github.com/ltfd-peq/ltfd-peq.github.io.git
cd ltfd-peq.github.io
hugo server        # abre em http://localhost:1313 e recarrega a cada mudança
```

Antes de abrir um pull request, rode as verificações:

```bash
pip install -r requirements.txt
python3 -I scripts/validar_dados.py
hugo build --environment provisorio --gc --minify --panicOnWarning
python3 -I scripts/checar_peso.py
```

O CI roda também a verificação de links (lychee) e os testes de acessibilidade no navegador
(`tests/verificar_paginas.py`, com axe-core e Playwright).

## Quero mudar X → edito Y

| Quero mudar… | Arquivo |
|---|---|
| Endereço, telefones, e-mail do laboratório, frase da página inicial | `data/laboratorio.yaml` |
| Uma linha de pesquisa (título, resumo, tópicos, docentes) | `data/linhas/<id>.yaml` |
| Dados de um membro (cargo, tema, orientação, Lattes, ORCID) | `data/membros/<id>.yaml` |
| Incluir um membro | criar `data/membros/<nome-sobrenome>.yaml` (copie um existente) |
| Marcos da trajetória (página Sobre) | `data/historico.yaml` (só com fonte) |
| Textos de Sobre, Pesquisa, Oportunidades, Privacidade, Acessibilidade | `content/pt/*.md` e `content/pt/<seção>/_index.md` |
| Assuntos da página de Contato | `content/pt/contato.md` (front matter `assuntos`) |
| Itens do menu | `config/_default/menus.pt.toml` |
| Rótulos da interface ("Menu", "Última atualização"…) | `i18n/pt.yaml` |
| Cores, tamanhos de fonte, espaçamentos | `assets/css/tokens.css` (rode `scripts/contraste.py`) |
| Aparência dos componentes | `assets/css/main.css` |
| Estrutura das páginas | `layouts/` |
| Logos, favicon, fontes | `static/` (fontes em `static/fonts/`, nunca em `assets/`) |
| Endereço do site (migração de domínio) | só o `baseURL` em `config/_default/hugo.toml` |

Regras de conteúdo: cada fato tem fonte (`fonte`, `verificado_em`); foto, e-mail de aluno e
destino de egresso só com autorização (`consentimento`); nada "a confirmar" vai ao ar.
Detalhes em `CLAUDE.md` e no plano do site.

## Estrutura

```
config/           configuração do Hugo (_default, provisorio = noindex, producao)
content/pt/       textos em Markdown; _content.gotmpl gera páginas a partir de data/
data/             laboratório, linhas, membros, trajetória (um YAML por registro)
schemas/          esquemas JSON dos dados (validados no CI)
layouts/          tema próprio (templates Hugo)
assets/           CSS (tokens + tema), JS do menu, ícones e imagens processadas pelo Hugo
static/           fontes, logos, favicons e imagem Open Graph, servidos como estão
scripts/          validação e verificações (Python); geração de fontes, ícones e logos
tests/            testes no navegador e configuração do verificador de links
docs/             decisões (ADR), campanha de implantação, revisão e comunicações
.github/          workflows (PR e publicação), Dependabot, CODEOWNERS
```

## Licenças

- Código: MIT (`LICENSE`).
- Textos do site: CC BY 4.0, salvo indicação em contrário [decisão pendente dos docentes].
- Marcas (LTFD, PEQ, COPPE, UFRJ), fotos de pessoas e fontes **não** estão sob essas licenças:
  as marcas seguem seus manuais de uso; a fonte Montserrat é distribuída sob a SIL Open Font
  License (`static/fonts/OFL-Montserrat.txt`).
