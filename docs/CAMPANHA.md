# Campanha de implantação do site do LTFD

Acompanhamento da execução do `PLANO_IMPLEMENTACAO_SITE_LTFD.md` (v1.3). Atualizar a cada
semana. **Situação em 23/10/2026: Fase 0 em curso; Fase 1, semana 1, com o código-base pronto.**

| Marco | Data | Situação |
|---|---|---|
| Decisões da Fase 0 (ou padrões aceitos) | 30/10/2026 | em aberto — ver §3 |
| Site provisório no ar, com `noindex`, para revisão | 06/11/2026 | depende da organização no GitHub (§2) |
| Revisão dos docentes (≈1–2 h cada) | 06 a 11/11/2026 | roteiro em `docs/revisao_mvp.md` |
| **Lançamento público** (ambiente `producao`) | **16/11/2026** | — |
| Onda A (Publicações, Projetos, Infraestrutura, busca) | até 18/12/2026 | — |
| Onda B (Teses, Egressos, Parceiros) | até 19/02/2027 | — |
| v1.0 e anúncio oficial | 05/03/2027 | — |

## 1. Pronto em 23/10/2026 (Claude Code, a revisar pelo professor)

Entregáveis da semana 1 do PLANO §12.3, e parte da semana 2:

- [x] Hugo 0.168.0 (edição padrão) instalado em `~/.local/bin`; projeto com ambientes
      `provisorio` (noindex) e `producao`; `CLAUDE.md`, `README.md`, `CHANGELOG.md`, `LICENSE`.
- [x] Repositório Git com o banco fora do Dropbox (ADR 0003). **Sem commits ainda.**
- [x] Tokens v0.3 ajustados ao manual da marca; 33 pares de cor verificados (`scripts/contraste.py`).
- [x] Tema: header com menu acessível (botão real, Esc, foco devolvido, resto da página inerte;
      sem JS, "Menu" leva ao mapa do site), cabeçalho de página, cards, rodapé e faixa institucional.
- [x] Marcas do manual otimizadas e conferidas pixel a pixel; favicons quadrados; imagem Open Graph;
      fontes Montserrat auto-hospedadas.
- [x] Páginas do lançamento: Início, Sobre, Pesquisa + 6 linhas, Equipe + 8 perfis, Oportunidades,
      Contato, Privacidade, Acessibilidade, 404 — com ligações cruzadas geradas dos dados.
- [x] `<head>` completo, JSON-LD (`ResearchOrganization`, `Person`, `BreadcrumbList`),
      `sitemap.xml`, `robots.txt` sem `Disallow`, CSP em `<meta>`.
- [x] Dados: `laboratorio`, 6 `linhas`, 8 `membros`, `historico` — cada fato com fonte (Lattes de
      2026, páginas do PEQ conferidas em 23/10/2026). Esquemas JSON e `validar_dados.py`.
- [x] Verificações locais todas verdes: dados (0 erros, 12 avisos = dados de alunos a coletar),
      contraste, peso (início: 168 KB em 11 requisições; meta 500 KB/25), marcadores (0),
      links internos e externos (0 quebrados), axe WCAG 2.2 AA (0 violações em 23 páginas,
      a 320 e 1280 px), sem rolagem lateral a 320 px, sem erros de console com a CSP ativa,
      menu pelo teclado. Menu horizontal cabe numa linha a 1024 px.
- [x] CI: `pr.yml` (bloqueia o merge) e `deploy.yml` (Pages pelo Actions, *cron* semanal),
      Actions fixadas por SHA, Dependabot mensal agrupado, `CODEOWNERS`, modelo de PR.

## 2. Depende do Prof. Gabriel nesta semana (até 30/10)

São ações externas (contas, e-mails, publicação): o Claude Code não as faz sem autorização.

1. [x] **Organização `ltfd-peq` criada no GitHub** (22/10/2026). Falta: exigir 2FA e convidar o
   2º docente como *owner* (§10.5).
2. Criar o repositório **público** `ltfd-peq.github.io` (nome exato), vazio: sem README,
   licença nem .gitignore.
3. No repositório: *Settings → Pages → Build and deployment → Source*: **GitHub Actions**
   (antes do primeiro *push*, para a primeira publicação já funcionar).
4. **Primeiro commit e push** — o Claude Code faz quando autorizado (a chave SSH desta máquina
   já autentica como GGSFerreira). O *push* dispara o workflow "Publicação", que publica o site
   provisório (com `noindex`) em `https://ltfd-peq.github.io/`.
5. *Settings → Rules*: *ruleset* do `main` com PR obrigatório, 1 aprovação, verificação
   "verificar" obrigatória, revisão de *code owners*; os 2 donos na lista de *bypass* (§10.5).
6. Criar a equipe `docentes` na organização (usada pelo `CODEOWNERS`).
7. Enviar a **consulta preliminar à TI do PEQ** — texto pronto em `docs/comunicacoes/consulta_ti_peq.md`.
8. Enviar o **formulário de equipe** (prazo 06/11) — perguntas em `docs/comunicacoes/formulario_equipe.md`.
9. Responder às decisões da Fase 0 (§3) ou aceitar os padrões já aplicados.
10. Avisar os docentes da revisão de 06 a 11/11 (roteiro em `docs/revisao_mvp.md`).

## 3. Decisões da Fase 0 — padrões já aplicados no código

Sem resposta até 30/10, vale o padrão (PLANO §15). Para mudar, edite o arquivo indicado.

| # (§15) | Decisão | Padrão aplicado | Onde mudar |
|---|---|---|---|
| 1 | Responsável e 2º docente dono | Prof. Gabriel; 2º docente a definir (risco R7) | organização no GitHub; `CODEOWNERS` |
| 5 | Licenças | Código MIT; textos CC BY 4.0 (marcas e fotos excluídas) | `LICENSE`, `README.md` |
| 6 | Coordenação e ano do nome "LTFD" | Sem "coordenação" e sem ano de fundação no site | `data/membros/*.yaml` (`funcao_ltfd`), `data/historico.yaml` |
| 7 | Papel de A. R. Secchi | Docente, com produção filtrada pela coautoria (§7.6) | `data/membros/argimiro-secchi.yaml` |
| 8 | Linhas de pesquisa | Proposta de 6; reologia dentro da linha 1 | `data/linhas/*.yaml` (`ativa: false` tira uma linha do ar) |
| 9 | Menu do lançamento | Sobre · Pesquisa · Equipe · Oportunidades · Contato | `config/_default/menus.pt.toml` |
| 10 | Kit visual | **Manual da marca 2026** (Montserrat, paleta oficial) — ver ADR 0002 | `assets/css/tokens.css` |
| 12 | Equipe do lançamento | 3 docentes + 5 orientandos dos Lattes (Barbara, César, Igor, Lauren, Leonardo); Alex V. L. Machado fora até confirmar o vínculo | `data/membros/` |
| 13 | Fotos e e-mails de alunos | Nenhum (iniciais no lugar da foto) | `consentimento` em cada membro |
| 15 | Sala, ramal, e-mail do laboratório | Endereço do kit (sem sala), telefones do PEQ, e-mail do Prof. Gabriel | `data/laboratorio.yaml` |
| 19 | Frase do hero e textos | Esqueletos do rascunho A, só com fatos com fonte; sem missão/visão | `data/laboratorio.yaml` (`proposta`), `content/pt/sobre.md` |
| 25 | Redes | Nenhuma no lançamento; GitHub institucional quando existir | `config/_default/hugo.toml` (`params.repositorio`) |
| 26 | Medição de audiência | GoatCounter, desligado até criar a conta | `params.goatcounter` |
| 31 | Nome em inglês | "Thermofluid Dynamics Laboratory" | `data/laboratorio.yaml` |
| 32 | Véu do hero | Bloco sólido (sem degradê) | `assets/css/tokens.css` (`--cor-veu-hero`) |
| 33 | Montserrat na web | **Adotada** (o manual a define como fonte institucional) | ADR 0002 |

## 4. Próximas tarefas de código

**Semana 2 (03 a 06/11)** — até o site provisório:

- [ ] Primeiro *deploy* provisório e conferência no endereço real (CSP, `noindex`, datas do Git).
- [ ] `scripts/checar_imagens.py` (rejeita EXIF/GPS e imagens grandes) antes de qualquer foto.
- [ ] `static/.well-known/security.txt` com `Expires` (e-mail do responsável).
- [ ] Meta de verificação do Search Console (parâmetro), a usar no lançamento.
- [ ] Mapa estático (C14) com botão "Carregar mapa interativo" — depois de conferir as coordenadas do Bloco G.
- [ ] GoatCounter com `count.js` servido pelo próprio site — depois de criada a conta.
- [ ] Textos curtos das linhas (perguntas de pesquisa, métodos) redigidos dos Lattes, com fonte, para a revisão.
- [ ] Lighthouse móvel medido à mão (Início, Equipe, Contato).

**Semana 3 (09 a 13/11):** correções da revisão; itens [L] do checklist do §13; no dia 16/11,
variável `HUGO_AMBIENTE=producao`, Search Console e sitemap.

**Onda A (até 18/12):** script de conversão do kit (`bib/ltfd.bib` com DOIs conferidos no
Crossref, projetos com `membros_ltfd` recalculado), páginas de Publicações, Projetos e
Infraestrutura, busca (Pagefind), vagas (`data/vagas/` + `vagas.js`), equipe completa.

## 5. Desvios do plano registrados

- ADR 0002 — design ajustado ao manual da marca (tipografia, paleta, logos, véu, cabeçalhos, favicons).
- ADR 0003 — banco do Git fora do Dropbox.
- Organização `ltfd-peq` (o plano previa `ltfd-ufrj`): endereço `https://ltfd-peq.github.io/`.
  Só o `baseURL` e a documentação mudaram; os caminhos das páginas são os mesmos (ADR 0001).
- O endereço do site fica em `config/_default/hugo.toml` (e não em `config/producao/`), porque
  o ambiente provisório usa o mesmo endereço; continua escrito num lugar só (§9.8).
- Testes de navegador em Python + Playwright (e não pa11y/Node), com axe-core 4.13.0 fixado; o
  Node entra só no CI, para baixar o axe.

## 6. Pontos de atenção

- A revisão dos docentes (06–11/11) é o caminho crítico (R19): textos curtos, roteiro pronto.
- `docs/revisao_mvp.md` lista cada fato publicado que precisa de olhar humano.
- O kit tem erros conhecidos (§7.4); nada do kit vai ao ar sem conferência (R2).
