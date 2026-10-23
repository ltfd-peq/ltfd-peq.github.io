# Formulário de equipe (prazo de resposta: 06/11/2026)

Perguntas para um formulário institucional (Google Forms ou Microsoft Forms da conta UFRJ).
As respostas e os termos assinados ficam **fora** do repositório do site (drive institucional
restrito aos docentes): o repositório é público e só recebe o que pode ir ao ar, já com o
consentimento registrado (PLANO §7.1, princípio 9, e §10.4).
Campos correspondentes: `data/membros/<id>.yaml` (PLANO §7.2).

## Mensagem de abertura

> O LTFD vai lançar seu site em 16/11/2026. Para a página da Equipe, precisamos de alguns dados
> seus. Só publicamos foto e e-mail de estudantes com sua autorização, que você pode retirar a
> qualquer momento. Prazo: 06/11.

## Perguntas

1. Nome completo (como deve aparecer no site).
2. Nome curto para os cards (opcional; ex.: "Paulo L. C. Lage").
3. Vínculo atual: docente · pesquisador(a)/engenheiro(a) de projeto · pós-doutorado · doutorado · mestrado · iniciação científica · TCC · técnico(a) · colaborador(a) externo(a).
4. Ano de início no LTFD (ou no curso).
5. Orientador(es) e coorientador(es) — ou supervisor(a), no pós-doutorado.
6. Título do trabalho (tese, dissertação, projeto de pós-doc ou de IC/TCC).
7. Linha(s) de pesquisa (lista com as 6 linhas).
8. ID Lattes (os 16 dígitos do endereço `lattes.cnpq.br/…`).
9. ORCID (obrigatório para doutorandos e pós-docs; recomendado no mestrado).
10. Google Acadêmico e GitHub (opcionais).
11. E-mail institucional para contato público (opcional).
12. Minibiografia de até 60 palavras (opcional; em português e, se quiser, em inglês).
13. **Autorizações** (cada uma separada; sem autorização, o site mostra as iniciais e não mostra e-mail):
    - [ ] Autorizo a publicação do meu e-mail institucional no site do LTFD.
    - [ ] Autorizo o uso da minha imagem (retrato padronizado) no site do LTFD. *(o termo de uso de imagem é assinado à parte, na sessão de fotos)*
    - [ ] Ao sair do LTFD, autorizo a publicação da minha atuação profissional na lista de egressos.

## Depois das respostas

- O editor transcreve para `data/membros/<id>.yaml` só o que foi autorizado, com
  `consentimento: {foto, email, destino, data}` e `fonte: "Formulário de equipe, <data>"`.
- `scripts/validar_dados.py` bloqueia qualquer e-mail, foto ou destino sem o consentimento correspondente.
