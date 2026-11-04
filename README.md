# QORE

QORE (Question Engine) é um aplicativo desktop local para coleta, extração,
classificação e gerenciamento de questões de concursos públicos.

## Status

O projeto está na etapa de fundação. A implementação é acompanhada pelas
[issues do repositório](https://github.com/joaocarlos2002/QORE/issues).

## Arquitetura planejada

- Desktop: Tauri, React e TypeScript.
- Backend local: Python e FastAPI.
- Persistência: SQLite, SQLAlchemy e Alembic.
- Processamento: PyMuPDF, OCR opcional e jobs assíncronos.

As decisões arquiteturais e os comandos oficiais de desenvolvimento serão
registrados antes da implementação das funcionalidades de domínio.

## Toolchain

- Python: `>=3.12,<3.15`
- Node.js: `>=22,<25`
- Gerenciador JavaScript: npm

Os comandos abaixo serão habilitados conforme os respectivos aplicativos forem
criados:

```powershell
npm install
npm run lint
npm run typecheck
npm test
npm run build
```

Para o backend:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest
```
