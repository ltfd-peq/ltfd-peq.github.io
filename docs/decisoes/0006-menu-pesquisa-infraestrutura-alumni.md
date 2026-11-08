# ADR 0006: Submenu de Pesquisa; Infraestrutura e Alumni no menu principal

- **Data:** 08/11/2026
- **Situação:** aceita (pedido do Prof. Gabriel G. S. Ferreira, 08/11/2026)
- **Revê:** PLANO §5.2 (decisão D1, "sem dropdown na v1") e ADR 0005 (endereços)

## Contexto

O professor pediu que o menu Pesquisa se dividisse em "Linhas de pesquisa" (as 5 linhas),
"Produção científica", "Repositórios de código aberto" e "Projetos de pesquisa", e que a
Infraestrutura fosse uma página separada. O PLANO evitava *dropdown* porque nenhuma
referência tinha um submenu acessível (`aria-expanded`, teclado).

## Decisões

- **Submenu acessível** no desktop, no padrão "disclosure navigation" do WAI-ARIA APG: o item
  Pesquisa vira um `<button aria-expanded aria-controls>` que abre a lista de subitens; Enter,
  Espaço e clique abrem e fecham; Esc fecha e devolve o foco ao botão; o submenu fecha quando
  o foco ou o clique saem dele. Sem hover, sem `role="menu"`. Só o item com
  `params.submenu = true` em `config/_default/menus.pt.toml` (hoje, Pesquisa) abre submenu;
  Equipe continua link simples.
- **Sem JavaScript**, o item continua um link para `/pesquisa/`, e os subitens estão no mapa do
  site do rodapé. No celular, os subitens aparecem sempre abaixo do item, como antes.
- **Páginas:** `/pesquisa/` virou a página-hub das quatro partes (destino sem JS e da trilha);
  as linhas e os métodos e ferramentas foram para `/pesquisa/linhas/`. As páginas de cada linha
  continuam em `/pesquisa/<id>/`, com a trilha "Pesquisa / Linhas de pesquisa / <linha>".
  "Artigos publicados" passou a se chamar "Produção científica" (mesmo endereço,
  `/pesquisa/publicacoes/`), e "Repositórios de código", "Repositórios de código aberto".
- **Infraestrutura** no 1º nível do menu, em `/infraestrutura/` (o endereço que o PLANO §5.1
  já previa).
- **Alumni** (pedido do mesmo dia): a lista de egressos sai de `/equipe/egressos/` e vira item
  próprio do menu, em `/alumni/`, logo depois de Equipe. Equipe deixa de ter subitens; o fim
  da página Equipe tem um link para Alumni. O menu fica com 7 itens, o máximo do PLANO §5.2,
  e ainda cabe numa linha a 1024 px.

## Consequências

- `assets/js/menu.js` ganhou o submenu; `tests/verificar_paginas.py` testa o submenu pelo
  teclado, roda o axe com ele aberto e confere que o menu cabe numa linha a 1024 px.
- Novo item com submenu: `params.submenu = true` no menu e subitens com `parent`.
