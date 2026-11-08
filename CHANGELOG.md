# Mudanças de estrutura

Registro de mudanças de tema, menus, dados e domínio (PLANO §11.5). Conteúdo do dia a dia
não entra aqui: ele fica no histórico do Git.

## 0.3.0 — 08/11/2026 — 2ª revisão do Prof. Gabriel G. S. Ferreira (anotações e `TO_DO`)

- **Linhas de pesquisa**: de 7 para 5 — escoamento reativo em reservatórios de petróleo (a
  principal, em primeiro); reologia de fluidos complexos (junta polímeros e suspensões); processos
  de separação e balanço populacional; CFD aplicada à garantia de escoamento (junta deslocamento
  em dutos e formação de hidratos); reatores não ideais em processos sustentáveis (junta
  membrana/hidrogênio e combustíveis de baixo carbono, com o Prof. Paulo L. C. Lage). Sai a
  palavra-chave "média volumétrica".
- **Coordenador sempre primeiro**: o Prof. Paulo L. C. Lage abre toda lista de docentes (Sobre,
  Contato, linhas, projetos).
- **Contato**: sem os cartões de assunto. Colaboração científica direto com os professores
  (coordenador primeiro, identificado); `ltfd@peq.coppe.ufrj.br` para problemas no site. A
  página de linha escreve aos docentes da linha; Oportunidades sem o botão "Escrever para o
  LTFD", com link para Contato. Sai o campo `email_cientifico` de `data/laboratorio.yaml`.
- **Equipe**: André Moreira de Castro (doutorado, orientação de Secchi) e a seção "Alunos de
  graduação", com Glauter Henrique Sotero Martins (Projeto Final, Profs. Argimiro e Gabriel).
- **Oportunidades**: "Vagas abertas" só aparece se houver vaga; sai a grade das linhas.
- **Pesquisa**: ferramentas com nome por extenso e link (OpenFOAM®, foam-extend, OpenPNM,
  Reaktoro) e aviso de marca do OpenFOAM®. Subpáginas novas (ADR 0005): Artigos publicados
  (`bib/ltfd.bib`, 100 artigos, `scripts/bib2json.py`), Repositórios de código
  (`data/software/`, 3), Projetos de pesquisa (`data/projetos/`, 33) e Infraestrutura
  (`data/equipamentos/`: cluster Apolo e sala dos alunos, com figuras).
- **Alumni** (egressos; item próprio do menu, `/alumni/`, `data/teses/`): 23 doutores e 36 mestres
  em Engenharia Química, do Lattes de Lage, títulos ainda sem link para o texto completo.
- **Menu** (ADR 0006): Pesquisa abre um submenu no desktop — Linhas de pesquisa
  (`/pesquisa/linhas/`, com métodos e ferramentas), Produção científica, Repositórios de código
  aberto e Projetos de pesquisa; `/pesquisa/` virou a página-hub dessas quatro partes.
  Infraestrutura e Alumni são páginas próprias no menu principal (`/infraestrutura/`, `/alumni/`;
  7 itens). Teste novo do submenu
  pelo teclado e do menu numa linha a 1024 px.
- Página de linha com figura e legenda (`imagem` em `data/linhas/`; `assets/img/pesquisas/`):
  reatores compactos na linha "Reatores não ideais em processos sustentáveis" e arenito Berea
  na linha "Escoamento reativo em reservatórios de petróleo".
- Mapa do site do rodapé com os subitens de Pesquisa e Equipe; corrigido o atributo espúrio
  (`ZgotmplZ`) nos subitens do menu.
- CI: `bib2json.py` antes do build; `validar_dados.py` valida as coleções novas.

## 0.2.0 — 08/11/2026 — revisão do Prof. Gabriel G. S. Ferreira e manual da marca v1.1

- **Linhas de pesquisa** redefinidas pela apresentação institucional do LTFD (30/05/2025):
  saem as 6 linhas anteriores e entram 7 — processabilidade de polímeros; processos de
  separação e balanço populacional; escoamento reativo em reservatórios de petróleo; reologia
  de misturas multifásicas complexas; deslocamento de fluidos miscíveis em dutos; reatores com
  membrana para produção de hidrogênio; reatores para combustíveis de baixo carbono. Docentes
  responsáveis pelos Lattes. Ícones novos: `linha-dutos` e `linha-membrana`.
- Hero, descrição e hub de Pesquisa sem restringir o software ao OpenFOAM (códigos próprios,
  OpenFOAM, foam-extend, OpenPNM, Reaktoro).
- **Equipe** em seções: Coordenador do laboratório (`data/laboratorio.yaml` → `coordenador`),
  Docentes, Pesquisadores (todos os vínculos juntos, com o vínculo sob o nome) e Corpo técnico.
  Novos registros: Alex Vinicius Lopes Machado (pesquisador) e Antônio Gonçalves Neto (corpo
  técnico). Leonardo de Souza Sá: orientação também do Prof. Gabriel G. S. Ferreira.
- **Contato**: e-mail geral `ltfd@peq.coppe.ufrj.br` (problemas no site, outros assuntos,
  rodapé, JSON-LD) e `paulo@peq.coppe.ufrj.br` para questões científicas (campo novo
  `email_cientifico`; sai `email_site`).
- Início: faixa de oportunidades com links para as abas de admissão do mestrado e do doutorado
  do PEQ (editais e inscrição).
- Sobre: sai a seção "Nossa trajetória" (os marcos continuam em `data/historico.yaml`); texto
  inclui a Engenharia de Petróleo e áreas afins.
- **Manual da marca v1.1** (ADR 0004): bordô só em detalhes; sobretítulos em preto; sem faixa
  bordô no cabeçalho de página e na imagem Open Graph; botão de destaque sem bordô; hero com 3
  bolhas bordô em vez de 16 vermelhas.
- Pendências da revisão em `PENDENCIAS.md`.

## 0.1.2 — 23/10/2026 — revisão do Prof. Paulo L. C. Lage

- E-mail de contato do laboratório: `paulo@peq.coppe.ufrj.br` ("Problemas no site" continua
  com o responsável pelo site).
- "Como chegar": lugares do Google Maps do LTFD e do PEQ (identificador e coordenadas em
  `data/laboratorio.yaml` → `locais`), com links para Google Maps e OpenStreetMap; coordenadas
  também no JSON-LD (`geo`, `hasMap`).
- Google Acadêmico de P. L. C. Lage no card e no perfil.
- Faixa institucional: logo do PEQ sem "COPPE/UFRJ" (a COPPE e a UFRJ aparecem ao lado);
  5,3 KB gzip em vez de 26,7 KB.

## 0.1.1 — 23/10/2026 — correção

- Página inicial: "Termofluidodinâmica" era cortada numa letra qualquer ("…dinâmic/a") a partir
  de ~1125 px. A palavra agora fica num bloco que desce inteiro para a linha de baixo e só é
  hifenizada nos `&shy;` quando não cabe; painel do hero de 40 para 44rem.
- Novo teste: nenhum título (H1–H3) com palavra partida fora de um ponto de hifenização, em
  7 larguras de 320 a 1920 px (`tests/verificar_paginas.py`).

## 0.1.0 — 23/10/2026 — esqueleto do MVP (Fase 1, semana 1)

- Hugo 0.168.0 (edição padrão), tema próprio e ambientes `provisorio` (noindex) e `producao`.
- Tokens de design v0.3, ajustados ao Manual de Identidade Visual do LTFD v1.0
  (Montserrat; paleta oficial) — ver `docs/decisoes/0002-manual-da-marca-2026.md`.
- Páginas do lançamento: Início, Sobre, Pesquisa e 6 linhas, Equipe e perfis, Oportunidades,
  Contato, Privacidade, Acessibilidade e 404.
- Dados: laboratório, 6 linhas (proposta padrão do PLANO §6.3), 3 docentes e 5 orientandos
  registrados nos Lattes, trajetória com fontes.
- `<head>` completo (title, description, canonical, Open Graph), JSON-LD
  (`ResearchOrganization`, `Person`, `BreadcrumbList`), `sitemap.xml`, `robots.txt`, CSP.
- Verificações: dados (esquemas, ids, consentimentos), contraste, peso, marcadores, links
  (lychee), axe/WCAG 2.2 AA, 320 px, console/CSP e menu pelo teclado.
- CI: `pr.yml` e `deploy.yml` (GitHub Pages pelo Actions), Actions fixadas por SHA, Dependabot.
