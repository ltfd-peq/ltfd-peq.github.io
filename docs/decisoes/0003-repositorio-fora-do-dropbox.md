# ADR 0003 — Banco de dados do Git fora do Dropbox/Insync

- **Data:** 23/10/2026
- **Situação:** aceita (implementa o PLANO §11.7)

## Contexto

A pasta de trabalho `0_Site_LTFD/5_Site_LTFD/` fica no Dropbox, sincronizado pelo Insync.
O plano (§11.7) alerta: "O repositório Git não deve ficar dentro do Dropbox/Insync: a
sincronização pode corromper o `.git`".

## Decisão

O repositório foi criado com `git init --separate-git-dir`:

- os arquivos do site continuam em `5_Site_LTFD/` (sincronizados, à vista dos docentes);
- o banco de dados do Git fica em `~/.local/share/ltfd-site/ltfd-peq.github.io.git`,
  fora da sincronização; em `5_Site_LTFD/.git` há só um arquivo-ponteiro (`gitdir: …`).

## Consequências

- Em outra máquina, o ponteiro não encontra o banco: lá, clone o repositório do GitHub numa
  pasta fora do Dropbox. O GitHub é a fonte; a cópia fria mensal (`git bundle`) vai para o
  drive institucional (§11.7).
- Nunca mover o diretório do Git para dentro do Dropbox nem sincronizá-lo.
- Para desfazer (por exemplo, migrar para uma pasta fora do Dropbox): clonar do GitHub
  depois do primeiro *push* e trabalhar no clone.
