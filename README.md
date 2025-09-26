# naFilaPlus — Backend (Flask)

API em Flask + SQLite + CORS. **O provedor de autenticação é o DummyJSON**.

---

## 🔧 Pré‑requisitos
- Docker

---

## 🚀 Build
```bash
docker rm -f nafila-backend 2>/dev/null || true
docker build -t nafila-backend .
```

## ▶️ Execução
Credenciais de teste:
- **username:** `emilys`
- **password:** `emilyspass`

```bash
docker run -d --name nafila-backend -p 5000:5000   -e EXTERNAL_AUTH_MODE=dummyjson   nafila-backend
```

### Teste rápido
```bash
curl -s http://127.0.0.1:5000/health
# -> {"status":"ok"}

curl -s -X POST http://127.0.0.1:5000/auth/login   -H 'Content-Type: application/json'   -d '{"email":"emilys","password":"emilyspass"}'
# -> 200 OK + {"message":"Login bem-sucedido","token":"..."}
```
---

## 📚 Endpoints
- `GET /health` → `{"status":"ok"}`
- `POST /auth/login` → autentica no DummyJSON
- `GET /contents` → lista conteúdos
- `POST /contents` → cria conteúdo
- `PUT /contents/:id` → atualiza (título/tipo/status/progresso)
- `DELETE /contents/:id` → remove

---

## 🧭 Fluxograma (Mermaid)

```mermaid
flowchart LR
    U[Usuário] --> FE[Frontend (HTML/CSS/JS)]
    FE -->|POST /auth/login<br/>username+password| BE[Backend Flask]
    BE -->|EXTERNAL_AUTH_MODE=dummyjson| DJ[DummyJSON /auth/login]
    DJ -->|token 200| BE
    BE -->|JSON {token}| FE

    FE -->|GET /contents| BE
    BE -->|SELECT| DB[(SQLite)]
    DB --> BE --> FE

    FE -->|POST/PUT/DELETE /contents| BE
    BE -->|INSERT/UPDATE/DELETE| DB
    DB --> BE --> FE
```

---


