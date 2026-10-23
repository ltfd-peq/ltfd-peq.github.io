# ADR 0002 — Ajustes do design ao Manual de Identidade Visual do LTFD (v1.0)

- **Data:** 23/10/2026
- **Situação:** proposta — vale até a revisão dos docentes (PLANO §15, itens 10, 29, 32 e 33)
- **Fontes:** `2_logo_LTFD_2026/Manual_Uso/manual_marca_LTFD.tex` (v1.0, outubro de 2026) e
  PLANO §8 (escrito em 22/10/2026, antes do manual)

## Contexto

O plano (v1.3) definiu Poppins + Source Sans 3, os tokens v0.2 e o uso dos logos do kit de
21/10/2026. O manual de marca, concluído depois, estabelece a família tipográfica, a paleta,
as seis variações de forma, as cinco de cor, tamanhos mínimos e áreas de proteção. Em questões
de marca, o manual prevalece; nas demais (acessibilidade, peso, estrutura), o plano.

## Decisões

| Tema | Plano (v1.3) | Adotado | Por quê |
|---|---|---|---|
| Tipografia | Poppins (títulos) + Source Sans 3 (texto); Montserrat fora da pilha web (§15, item 33) | **Montserrat** em títulos e texto (variável 400–800 + itálico 400), Arial/Helvetica como alternativa | O manual define a Montserrat como família institucional, inclusive para texto, e indica Arial/Helvetica na falta dela. Uma família só atende "sem variações de fonte" (briefing de 2025). Peso: 38 KB (latin) + 19 KB (itálico, só se a página usar) |
| Paleta | Azul `#003366`, vinho `#8A2432`, vermelho `#A61E29` (item ativo), `#CC1B21` (decorativo) | Azul LTFD `#003366`, Bordô LTFD `#8A2432`, Azul profundo `#022C53`, Preto 90 % `#1A1A1A`; saem `#A61E29` e `#CC1B21` | São as cores do manual; as outras duas não constam dele. O filete do item ativo passa a bordô (8,83:1) |
| Texto corrido | `#333333` | `#1A1A1A` (Preto 90 % do manual) | Cor de texto do próprio manual; 17,4:1 |
| Rodapé | `#061A2E` | Azul profundo `#022C53` | Cor da marca; branco a 14,12:1; logo negativo permitido em fundo escuro |
| Logo no header | Horizontal compacta do kit, 32/40 px de altura | **Reduzida** (símbolo + sigla), 34 px (celular) e 38 px (desktop) = 116–130 px de largura | O manual indica a reduzida para "barras de navegação", com mínimo de 110 px. A horizontal exigiria ≥ 220 px de largura (67 px de altura) e não cabe num header de 56–64 px com a área de proteção |
| Faixa institucional | LTFD · PEQ · COPPE · UFRJ (sigla do kit) | LTFD na versão **horizontal colorida** (230 px) + PEQ, COPPE e UFRJ | Horizontal é a versão do manual para "faixas"; mínimo de 220 px |
| Rodapé, coluna 1 | Sigla LTFD branca | Nome do laboratório em texto | Evita o terceiro logo na mesma tela e a sigla como imagem pequena |
| Véu do hero | Degradê (§15, item 32) | **Bloco sólido** `#022C53` a 85 % atrás do texto | Alternativa já prevista no plano; respeita "sem degradê"; pior caso 9,0:1 |
| Cabeçalho das páginas internas | Arte `cabecalho-*` do kit com o H1 sobre a metade escura | **Faixa azul sólida** com filete bordô na base | As artes do kit têm degradê; a faixa sólida garante o contraste (§3.6). O filete ecoa a capa do manual (azul com faixa bordô) |
| Favicon | `favicon-simplificado.svg` do kit | Símbolo do manual (`aplicacoes/favicon.svg`), `.ico` e PNGs **regerados quadrados** | Os PNG/ICO do manual saem com 16×17, 32×33 e 180×187 px (proporção do símbolo). `scripts/gerar_icones.py` centraliza o símbolo num quadrado, sem deformar |
| Imagem Open Graph | `og-image` do kit | Gerada da marca vertical negativa sobre azul, com faixa bordô (`scripts/gerar_og.py`) | Mesma composição da capa do manual; usa só arquivos oficiais |
| Peso dos SVG | Meta de `svgo` (§8.5) | `scripts/otimizar_svg.py` (2 casas decimais, estilos em atributos) + `scripts/comparar_svg.py` (≤ 0,1 % de pixels diferentes) | Sem Node no projeto. Header 12,9 KB gzip (meta 25); institucionais somam 68 KB gzip (meta 60: pendência) |

## Pendências

- Aprovação dos docentes (item 10 do §15) — especialmente a troca de tipografia.
- Os três logos institucionais passam 8 KB da meta de 60 KB gzip (UFRJ = 38 KB). Opções: PNG/WebP
  em 2× só para a UFRJ, ou pedir à SGCOM um vetor mais leve. O orçamento da página continua folgado.
- Arquivos oficiais do PEQ e da UFRJ: os vetores do kit são extrações/vetorizações (README do kit).
