# ADR 0001 — Hugo + tema próprio + GitHub Pages

- **Data:** 23/10/2026
- **Situação:** aceita (decisões da versão 1.3 do plano; §15, itens 2, 3 e 5)
- **Fonte:** `PLANO_IMPLEMENTACAO_SITE_LTFD.md` §9 (a matriz completa está no rascunho B, §3)

## Contexto

Os 5 sites de referência (LabCFD, PAM, LADES, ATOMS, LRAP) usam HTML à mão, Google Sites,
WordPress e Wix; todos têm links quebrados, informação vencida e problemas de contraste, e
dois estão parados. Nenhum usa gerador estático com dados versionados (0/5). O site precisa
ser mantido por alunos que se revezam, sem servidor para atualizar.

## Decisão

- **Hugo 0.168.x, edição padrão**, versão fixa no CI e atualização semestral num PR.
- **Tema próprio** enxuto, sem frameworks; dados em YAML (um arquivo por registro) e
  publicações em BibTeX curado (Onda A).
- **GitHub Pages** na organização `ltfd-peq`, repositório `ltfd-peq.github.io` (site na
  raiz), publicado pelo GitHub Actions. Endereço de lançamento: `https://ltfd-peq.github.io/`.
  O plano (v1.3) previa a organização `ltfd-ufrj`; ela foi criada como **`ltfd-peq`** em
  22/10/2026, e o endereço mudou junto. Como o endereço só está no `baseURL`, nada mais muda.
- Domínio e hospedagem definitivos ficam para a migração planejada (§9.8): o endereço do site
  está escrito só no `baseURL`, e os caminhos não mudam.

## Matriz (resumo)

Hugo 92,4/100; Quarto 78,2 (plano B); Jekyll + al-folio 73,8; Astro 73,6; Hugo Blox 71,6;
HTML à mão 61,0; WordPress 48,0; Google Sites 47,6; Wix 40,0. O Hugo fica em 1º nos 6
cenários de sensibilidade.

## Gatilhos do plano B

- No marco de 06/11/2026, se o tema se mostrar difícil demais para quem vai mantê-lo: Quarto
  1.10.x, reaproveitando `data/`, imagens, CI e hospedagem.
- Se o PEQ exigir hospedagem institucional ou cabeçalhos HTTP: mesma pasta `public/` num
  *virtual host* isolado (cenário B do §9.8).
