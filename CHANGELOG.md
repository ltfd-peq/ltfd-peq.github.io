# Mudanças de estrutura

Registro de mudanças de tema, menus, dados e domínio (PLANO §11.5). Conteúdo do dia a dia
não entra aqui: ele fica no histórico do Git.

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
