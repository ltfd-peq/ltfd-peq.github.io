# Pendências do site do LTFD

Dados que precisam ser conferidos ou coletados antes de ir ao ar. Origem: revisões do
Prof. Gabriel G. S. Ferreira de 08/11/2026 (1ª rodada e 2ª rodada, com o `TO_DO`), salvo
indicação. Ao resolver um item, marque-o, atualize o YAML correspondente (com `fonte` e
`verificado_em`) e registre no PR.

## Contato

- [ ] **Conferir os telefones** do rodapé e da página Contato: (21) 3938-8349,
      (21) 3938-8304 e (21) 3938-1575, hoje apresentados como da secretaria do PEQ.
      Ver também se o LTFD tem ramal próprio. Arquivo: `data/laboratorio.yaml` → `telefones`.
- [ ] **Testar o e-mail `ltfd@peq.coppe.ufrj.br`** (envio de teste) antes do lançamento de
      16/11/2026: ele recebe "Problemas no site" e é o e-mail do rodapé.

## Equipe: currículos Lattes

- [ ] Buscar o link do currículo Lattes (16 dígitos, campo `ids.lattes`) de cada membro que
      ainda não tem:
  - [ ] Barbara de Farias Esteves
  - [ ] César Gustavo Timaná Beteta
  - [ ] Igor Nardi Caxiano
  - [ ] Lauren Schlatter Fernandes
  - [ ] Leonardo de Souza Sá
  - [ ] André Moreira de Castro
  - [ ] Glauter Henrique Sotero Martins (o Lattes dele usa o identificador antigo
        `K2873493P1`; abrir o currículo e copiar o número de 16 dígitos)
  - [ ] Antônio Gonçalves Neto (se houver)

  Os ORCID dos pesquisadores, pós-doutorandos e doutorandos também faltam
  (`python3 -I scripts/validar_dados.py` lista).

## Equipe: outros dados

- [ ] **Alex Vinícius Lopes Machado:** ano de início como pesquisador. A grafia "Vinícius"
      e a linha "Escoamento reativo em reservatórios" vêm do Lattes de Lage e dos artigos;
      confirmar.
- [ ] **Antônio Gonçalves Neto:** cargo ou função (hoje aparece "Técnico(a)" sob o nome) e
      ano de início.
- [ ] **André Moreira de Castro:** o doutorado é em Engenharia de Processos Químicos e
      Bioquímicos (Escola de Química/UFRJ), não no PEQ, com orientação de Secchi desde 2019
      (Lattes de Secchi). Confirmar a linha "Reologia de fluidos complexos".
- [ ] **Glauter Henrique Sotero Martins:** título e ano de início do Projeto Final. Linha
      "Reatores não ideais" atribuída pela IC concluída em 2025 (reatores tubulares para
      hidrogênio).
- [ ] **Leonardo de Souza Sá:** confirmar se o Prof. Gabriel é orientador ou coorientador do
      doutorado. Hoje o site mostra "Orientação: Paulo L. C. Lage e Gabriel G. S. Ferreira";
      no mestrado (concluído em 2026) foi coorientação.
- [ ] **Barbara de Farias Esteves:** título do projeto de pós-doutorado.

## Linhas de pesquisa

- [ ] Confirmar os docentes responsáveis pelas 5 linhas (o coordenador aparece sempre
      primeiro):

  | Linha | Docentes no site |
  |---|---|
  | Escoamento reativo em reservatórios de petróleo (principal) | Lage, Ferreira |
  | Reologia de fluidos complexos | Lage, Secchi, Ferreira |
  | Processos de separação e balanço populacional | Lage, Ferreira |
  | CFD aplicada à garantia de escoamento | Lage, Ferreira. Secchi tem trabalhos sobre formação de hidratos em linhas de produção (ex.: Guedes et al., CHERD, 2026): entra? |
  | Reatores não ideais em processos sustentáveis | Lage, Secchi, Ferreira |

- [ ] Imagens das linhas: "Reatores não ideais" tem a figura dos reatores compactos e
      "Escoamento reativo em reservatórios", a do arenito Berea (`assets/img/pesquisas/`).
      Falta a legenda técnica delas (caso, modelo, solver; PLANO §6.4) e o crédito, se houver. Para as outras linhas, a apresentação tem figuras de
      resultados: usar só as do LTFD que não estão sob direitos de editora, com legenda e fonte.

## Pesquisa: métodos e ferramentas

- [ ] "Incluir as siglas do OpenFOAM, OpenPNM e Reaktoro": entraram os nomes por extenso
      (OpenFOAM = Open Source Field Operation and Manipulation; OpenPNM = Open Pore Network
      Modeling; Reaktoro não é sigla) e os links. Se a ideia era pôr os **logos**, é preciso
      conferir antes a política de marca de cada projeto: a do OpenFOAM® restringe o uso.

## Artigos publicados (`bib/ltfd.bib`)

- [ ] Cada docente confere a própria lista (PLANO §7.7, passo 4). São 100 artigos (há
      coautorias entre os docentes): 95 de Lage, 5 de Ferreira e 10 de Secchi com coautor do
      LTFD; 98 com DOI conferido no Crossref.
      Pontos levantados na conferência:
  - André M. de Castro aparece como "CASTRO, ANDRÉ M." em 3 artigos de Secchi
    (castro2018application, silva2020morphological, pereira2020estimation; reômetro
    multipasse). O de 2018 é anterior ao doutorado dele (2019): entra?
  - moraes2021optimal (IFAC-PapersOnLine): periódico no Lattes de Lage, congresso no de
    Secchi. Entrou como artigo.
  - monteagudo2001extending ficou sem DOI: o candidato 10.1016/S0378-3812(01)00530-1 tem os
    mesmos autores, volume e páginas, mas o título no Crossref está truncado.
  - Em 6 artigos o ano é o da edição impressa (o Lattes traz o da publicação online):
    favero2024simulating, moraes2020mass, santos2020gpuaccelerated, charin2019dynamic,
    sampaio2017nonisothermal, favero2012dualquadrature.
  - Lattes de Lage a corrigir: a Parte I do IJHMT 2004 aparece só com Lage (no Crossref,
    Ribeiro e Lage); SPE J. 2025 e BJChE 2025 (Sá) têm volume e páginas provisórios.
- [ ] Definir o ano em que o nome "LTFD" passou a ser usado: os artigos anteriores ficariam
      com `escopo = historico-area-tfd` (hoje todos estão como `ltfd`).

## Projetos (`data/projetos/`)

- [ ] Cada docente confere os próprios projetos. Pontos levantados na extração:
  - Coordenados por Secchi, com Lage ou Ferreira como integrante, mas fora da
    termofluidodinâmica (PLANO §7.6): SOFGTL, Separação de Enantiômeros, Associação
    PEQ–PLAPIQUI e (R)-Praziquantel. Ficam ou saem?
  - Ficaram de fora e podem entrar: Reforma a vapor de gás natural (2021–2024; perto de
    hidrogênio), Desidratação de bioetanol a eteno (3 projetos, 2014–2023), Extrusão e
    coextrusão de poliestireno (2003–2008, UFRGS), reatores de polimerização e de hidrogenação.
  - "Termofluidodinâmica: Modelagem e Simulação de Escoamentos Complexos" (Lage) consta
    "em andamento" desde 2016: confirmar.
  - "Caracterização de Fluidos Complexos… sob CO2": início 2021 no Lattes de Ferreira e 2022
    no de Lage (usado 2022). "Simulações Computacionais de Alta Complexidade" e "Modelagem de
    Escoamentos Multifásicos": "em andamento" com ano final no Lattes de Lage (usado o ano
    final).
  - Um título está em caixa alta no Lattes ("CARACTERIZAÇÃO DE FLUIDOS COMPLEXOS…").
  - Projetos industriais: só título, período, coordenação e financiadores (públicos no
    Lattes). Descrições, só depois de conferir com os coordenadores e a COPPETEC.

## Alumni — egressos (`data/teses/`)

- Só entram trabalhos de **Engenharia Química** (revisão de 08/11/2026). Saíram 9: Engenharia
  de Processos Químicos e Bioquímicos/UFRJ (Raphael M. L. Coelho, D 2006; Nathalia C. de Sá,
  D 2026; Tatiana P. Sampaio, M 2014; Victor Corcino de Albuquerque, M 2021), Engenharia
  Mecânica/UFRJ (Manuel A. H. Bolivar, M 1996; Umberto Sansoni Júnior, M 2005; Yuri P. de
  Almeida, M 2015), Padova (Enrico Favaro, M 2013) e Biskra (Khaled Athmani, D 2022).
- [ ] **Links das dissertações e teses** (`link_repositorio`): localizar cada trabalho no
      repositório da UFRJ (Pantheon) ou no portal do PEQ. Hoje os 59 títulos aparecem sem link.
- [ ] João Victor de Moraes Silva (M 2025) é de Engenharia Química da **UERJ** (coorientação de
      Lage): fica, pela regra acima, ou sai por não ser da UFRJ?
- [ ] Coorientações de Lage sem o orientador principal escrito em nenhum Lattes: Willian M.
      Poubel (D 2013) e João Victor de Moraes Silva (M 2025, UERJ).
- [ ] Samel Moraes (M 2011): Secchi registra-se orientador, com outro título; não entrou.
- [ ] Títulos diferentes nos Lattes de Lage e de Ferreira: Lauren (em português no de
      Ferreira), Manoela e Matheus A. R. da Silva. Vale o de Lage; conferir.
- [ ] Título em caixa alta no Lattes (Bárbara de Farias Esteves) e "sa/se" no
      doutorado de Livia Jatobá: corrigir no Lattes ou aqui.
- [ ] Egressos de Secchi e de Ferreira (orientações principais) ainda não entraram.

## Repositórios de código (`data/software/`)

- [ ] **Licenças:** "An Improved Suspension Balance Model" e "Corrected micro-continuum"
      derivam do OpenFOAM (GPL-3.0), mas estão sob CC-BY-SA-4.0, que não é licença de software
      e provavelmente é incompatível com a GPL. "Sub-volume analysis" não tem licença
      declarada (o site mostra "não declarada"): sem licença, ninguém pode reutilizar o código.
- [ ] Os três estão em contas pessoais; o PLANO §6.11 prevê a organização institucional
      (`ltfd-peq`).
- [ ] Candidato futuro: `alexvlmachado/cmc-reactive-transport` (código sai com o artigo).
      Privados hoje, entram quando abertos e ligados a artigo: solvers de César (redes de
      poros), Leonardo (PermOpenPNM), Igor, Ferreira e do grupo process-intensification.

## Infraestrutura (`data/equipamentos/`)

- [ ] **Figura do cluster Apolo:** `apolo-rack.png` foi gerada por IA (ChatGPT/gpt-image,
      segundo os metadados C2PA) a partir da foto `apolo.jpeg`; o site não informa isso. Se
      preferir a foto real, ela tem a ponta de uma mão no canto inferior direito (recortar).
- [ ] Dados do Apolo: só os nós de computação (`apolo-simple-description`). Faltam, se for o
      caso, nó de login, armazenamento, rede de interconexão, GPUs, ano e financiamento.
- [ ] **Sala dos alunos:** a figura `sala_alunos.png` também foi gerada por IA (ChatGPT/gpt-image,
      segundo os metadados C2PA; o original ficou em `inspiration/Infraestrutura/`); o site não
      informa isso. Faltam dados da sala (número de lugares, computadores) e, se quiser, uma
      foto real: só sem pessoas identificáveis ou com termo de uso de imagem, e sem EXIF/GPS.
- [ ] Unidades experimentais (coluna de bolhas, evaporação por contato direto): seguem
      ativas? Se sim, entram com foto, faixa de operação e responsável.

## Da apresentação institucional, para as próximas ondas

- Parceiros acadêmicos e empresas: página Parceiros da Onda B (nomes, sem logos de terceiros
  sem autorização).
- Colaboradores do LabCFD/EQ/UFRJ (Luiz F. Silva e Fabio Santos): seção "Colaboradores
  externos" da Equipe, com nome completo e Lattes.
