# naFilaPlus — Backend (Flask)

API em Flask com SQLite e CORS. Autenticacao externa fixa via DummyJSON.

Credenciais publicas para teste:
- username: `emilys`
- password: `emilyspass`

---

## Build & Run
```bash
docker rm -f nafila-backend 2>/dev/null || true
docker build -t nafila-backend .
docker run -d --name nafila-backend -p 5000:5000 nafila-backend
```

### Teste rapido
```bash
# Saude
curl -s http://127.0.0.1:5000/health
# Login (usa username no campo "email")
curl -s -X POST http://127.0.0.1:5000/auth/login   -H 'Content-Type: application/json'   -d '{"email":"emilys","password":"emilyspass"}'
```

O backend responde `{"message":"Login bem-sucedido","token":"..."}` ao autenticar no DummyJSON.

---

## Endpoints
- GET /health -> {"status":"ok"}
- POST /auth/login -> autentica no DummyJSON e retorna token
- GET /contents -> lista conteudos
- POST /contents -> cria conteudo
- PUT /contents/:id -> atualiza
- DELETE /contents/:id -> remove

---

## Fluxograma (Mermaid)
```mermaid
flowchart LR
  U[Usuario] --> FE[Frontend]
  FE -->|POST /auth/login — username,password| BE[Backend Flask]
  BE -->|chama| DJ[DummyJSON /auth/login]
  DJ -->|200 + token| BE
  BE -->|JSON { token }| FE

  FE -->|GET /contents| BE
  BE -->|SELECT ...| DB[(SQLite)]
  DB --> BE --> FE

  FE -->|POST/PUT/DELETE /contents| BE
  BE -->|INSERT/UPDATE/DELETE| DB
  DB --> BE --> FE
```

---
