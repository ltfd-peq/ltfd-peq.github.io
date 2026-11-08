# ADR 0005: Subpáginas de Pesquisa e Egressos antecipadas para o lançamento

- **Data:** 08/11/2026
- **Situação:** aceita (2ª revisão do Prof. Gabriel G. S. Ferreira, 08/11/2026, arquivo `TO_DO`
  em `bugs-to-fix/`, fora do repositório)
- **Complementa:** PLANO §5.1, §6.5, §6.6, §6.8, §6.9 e §6.11; ADR 0001. Endereços e menu
  revistos pelo ADR 0006 (Infraestrutura em `/infraestrutura/`, Egressos como "Alumni" em `/alumni/`,
  submenu de Pesquisa)

## Contexto

O PLANO deixava Publicações, Projetos e Infraestrutura para a Onda A (até 18/12/2026) e
Egressos e Software para a Onda B e a v1.1. Na revisão, o professor pediu essas páginas já
no lançamento:

- subpáginas de **Pesquisa** com os artigos publicados, os repositórios públicos de código
  dos artigos, os projetos (concluídos e em andamento) e a infraestrutura física, com fotos;
- página de **Egressos**, com a lista do Lattes do Prof. Paulo L. C. Lage e os links das
  dissertações ainda inativos.

## Decisões

| Ponto | PLANO | Agora |
|---|---|---|
| Endereços | `/publicacoes/`, `/projetos/`, `/infraestrutura/`, `/software/` (planos, fora de Pesquisa) | `/pesquisa/publicacoes/`, `/pesquisa/repositorios/`, `/pesquisa/projetos/`, `/pesquisa/infraestrutura/`: são subpáginas de Pesquisa, como o professor pediu, e a trilha mostra "Início / Pesquisa / …". Egressos fica em `/equipe/egressos/`, como no plano |
| Menu | Publicações no 1º nível a partir da Onda A | Menu de 1º nível sem mudança. As subpáginas aparecem no hub de Pesquisa, no painel móvel e no mapa do site do rodapé |
| Publicações | `bib/ltfd.bib` curado + `bib2json.py` (D2) | Igual. `scripts/bib2json.py` gera `data/gerado/publicacoes.json` antes do Hugo, no CI e localmente; `data/gerado/` fica fora do Git. Formato compacto próprio, um H2 por ano, autores do LTFD em negrito pelo campo `membros`, DOI conferido no Crossref e exportação BibTeX da lista inteira |
| Escopo das publicações (§7.6) | Itens com autor do LTFD na data; Secchi só com coautor do LTFD | Todos os artigos de Lage; os de Ferreira desde 2020 ou com Lage; os de Secchi com coautor do LTFD. `escopo = ltfd` em todos, porque o ano do nome "LTFD" não foi definido |
| Egressos | Membros com `periodo.fim` + `data/teses/` | Só `data/teses/<id>.yaml` (um registro por trabalho defendido), sem perfil por egresso. Por enquanto vem do Lattes de Lage; `link_repositorio: null` deixa o título sem link |
| Projetos | Filtros por situação, financiador, linha e natureza | Sem filtros por enquanto (sem JS novo): em andamento primeiro, concluídos por década. Situação calculada por `fim` |
| Software | `/software/`, v1.1, a partir de 2 itens | "Repositórios de código": só repositório público ligado a artigo com DOI (`data/software/`) |
| Infraestrutura | Tabela por recurso; foto por unidade | `data/equipamentos/` com especificações em tabela. Só o cluster Apolo, com os dados enviados pelo professor; os clusters antigos da apresentação saíram por estarem defasados. As figuras do Apolo e da sala dos alunos foram geradas por IA; a origem fica registrada no campo `fonte` dos dados, e o site as mostra sem legenda (pedido do professor, 08/11/2026) |

## Consequências

- O CI roda `bib2json.py` antes do build (`pr.yml` e `deploy.yml`); quem roda o site
  localmente também precisa rodá-lo (README, CLAUDE.md).
- `validar_dados.py` valida as coleções `teses`, `projetos`, `software` e `equipamentos`.
- O que falta conferir em cada lista está em `PENDENCIAS.md`.
