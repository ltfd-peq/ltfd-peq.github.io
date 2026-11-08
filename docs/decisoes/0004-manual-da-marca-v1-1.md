# ADR 0004 — Ajustes ao Manual de Identidade Visual do LTFD v1.1

- **Data:** 08/11/2026
- **Situação:** aceita (revisão do Prof. Gabriel G. S. Ferreira, 08/11/2026)
- **Fontes:** Manual de Identidade Visual do LTFD v1.1 (novembro de 2026), aplicado pela
  skill `marca-ltfd`; anotações em `bugs-to-fix/` (fora do repositório)
- **Complementa:** ADR 0002 (manual v1.0)

## Contexto

A v1.1 do manual restringe o Bordô LTFD (`#8A2432`) a detalhes — fios, marcadores, ícones,
pequenos elementos gráficos — e o proíbe em blocos de texto, subtítulos, rótulos, botões com
texto, faixas e grandes áreas. Capas passam a ser em fundo branco com a marca colorida; capa
em Azul LTFD com a negativa continua permitida, mas sem faixa bordô. Os logos não mudaram.
Na revisão do site, o professor pediu menos vermelho nas figuras.

## Decisões

| Elemento | Antes (ADR 0002) | Agora |
|---|---|---|
| Sobretítulos ("LINHAS DE PESQUISA", "EQUIPE"…) | Texto bordô | Preto 90 % (`--cor-sobretitulo`) |
| Cabeçalho das páginas internas | Faixa azul com filete bordô de 4 px na base | Faixa azul sólida, sem filete |
| Botão de destaque | Fundo bordô com texto branco | No fundo claro, igual ao botão padrão (azul); em superfície azul, branco com texto azul |
| Selos de tipo | Texto bordô sobre `#F6E9EB` | Azul LTFD sobre azul-gelo; sai `--ltfd-bordo-gelo` |
| Imagem Open Graph | Azul, marca negativa e faixa bordô na base | Azul e marca negativa, sem faixa |
| Hero (arte do kit) | 16 bolhas e um fio em `#A61E29` (fora do manual) | 3 bolhas e o fio em Bordô LTFD; as outras 13 nos azuis do próprio desenho |
| Ícones das linhas | Até 3 elementos bordô por ícone | 1 elemento bordô por ícone |

Continuam em bordô, como detalhe: o filete sob os títulos de seção (`.titulo-secao h2::after`),
o filete do item de menu ativo e o elemento de destaque de cada ícone.

## Consequências

- `scripts/contraste.py`: saem os pares de texto bordô; entram preto sobre branco e fundo
  alternado (sobretítulos) e azul sobre branco (botão de destaque em superfície azul).
- Quem criar componente novo usa `--cor-acento` só em fios, marcadores e ícones.
