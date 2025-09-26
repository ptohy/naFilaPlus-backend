  # naFilaPlus — Backend (Flask)

  API em Flask com SQLite e CORS. A autenticação externa está **fixada em DummyJSON** por padrão (recomendado para avaliação).

  ---

  ## 🔧 Pré‑requisitos
  - Docker

  ---

  ## 🚀 Build
  ```bash
  docker rm -f nafila-backend 2>/dev/null || true
  docker build -t nafila-backend .
  ```

  ## ▶️ Execução (recomendado) — **DummyJSON**
  O DummyJSON usa **username** no lugar de e‑mail. Credenciais públicas e estáveis:
  - **username:** `emilys`
  - **password:** `emilyspass`

  ```bash
  docker run -d --name nafila-backend -p 5000:5000 nafila-backend
  ```

  Teste rápido:
  ```bash
  curl -s http://127.0.0.1:5000/health
  curl -s -X POST http://127.0.0.1:5000/auth/login \
-H 'Content-Type: application/json' \
-d '{"email":"emilys","password":"emilyspass"}'
  ```

  > ℹ️ Se você **explicitamente** quiser usar ReqRes (autentica por *e‑mail*), exporte `EXTERNAL_AUTH_MODE=reqres` e esteja ciente de que o endpoint público do ReqRes pode devolver `401`.
  >
  > **Padrão do projeto para avaliação: DummyJSON.**

  ---

  ## 🔌 Variáveis de ambiente
  - `EXTERNAL_AUTH_MODE` — provedor externo: `dummyjson` (default) ou `reqres`.
  - `EXTERNAL_AUTH_URL` — sobrescreve a URL do provedor (opcional).
    - *Default (dummyjson):* `https://dummyjson.com/auth/login`

  Exemplo via `--env-file`:
  ```bash
  docker run -d --name nafila-backend -p 5000:5000 --env-file .env nafila-backend
  ```

  ---

  ## 📚 Endpoints
  - `GET /health` → `{"status":"ok"}`
  - `POST /auth/login` → autentica no provedor externo
  - `GET /contents` → lista conteúdos (filtros opcionais `?status=&tipo=`)
  - `POST /contents` → cria conteúdo
  - `PUT /contents/:id` → atualiza
  - `DELETE /contents/:id` → remove

  ---

  ## 🔀 Fluxograma (Mermaid)
  ```mermaid
  flowchart LR
    U[Usuário] --> FE[Frontend]
    FE -->|POST /auth/login (username,password)| BE[Backend Flask]
    BE -->|DummyJSON| DJ[https://dummyjson.com/auth/login]
    DJ -->|200 token| BE
    BE -->|{token}| FE

    FE -->|GET /contents| BE
    BE -->|SELECT| DB[(SQLite)]
    DB --> BE --> FE

    FE -->|POST/PUT/DELETE /contents| BE
    BE -->|INSERT/UPDATE/DELETE| DB
    DB --> BE --> FE
  ```

  ---

  ## ✅ Checklist de requisitos (MVP)
  - [x] Healthcheck (`/health`)
  - [x] Login integrado a serviço público (DummyJSON)
  - [x] CRUD completo com SQLite
  - [x] CORS habilitado (frontend consome a API)
