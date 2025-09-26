# naFilaPlus — Backend (Flask)

API em **Flask + SQLite + CORS**. Para a avaliação do MVP, **somente o provedor DummyJSON** é utilizado para autenticação externa (estável e público).

---

## 🔧 Pré‑requisitos
- Docker

---

## 🚀 Build
```bash
docker rm -f nafila-backend 2>/dev/null || true
docker build -t nafila-backend .
```

## ▶️ Execução (padrão recomendado — DummyJSON)
O DummyJSON usa **username** no lugar de e‑mail. Credenciais públicas e estáveis:
- **username:** `emilys`
- **password:** `emilyspass`

```bash
docker run -d --name nafila-backend -p 5000:5000 nafila-backend
```
> A imagem já inicia usando **DummyJSON** por padrão, não é necessário setar variáveis.

Teste rápido:
```bash
curl -s http://127.0.0.1:5000/health
curl -s -X POST http://127.0.0.1:5000/auth/login   -H 'Content-Type: application/json'   -d '{"email":"emilys","password":"emilyspass"}'
# -> 200 OK + {"message":"Login bem-sucedido","token":"..."}
```

---

## 🔌 Variáveis de ambiente (opcional)
- `EXTERNAL_AUTH_URL` — sobrescreve a URL do provedor externo (padrão: `https://dummyjson.com/auth/login`).

> Por padrão nada precisa ser configurado. O backend já autentica no DummyJSON
> com `username` e `password` (ex.: `emilys / emilyspass`).

---

## 📚 Endpoints
- `GET /health` → `{"status":"ok"}`
- `POST /auth/login` → autentica no DummyJSON
- `GET /contents` → lista conteúdos (filtros opcionais `?status=&tipo=`)
- `POST /contents` → cria conteúdo
- `PUT /contents/:id` → atualiza
- `DELETE /contents/:id` → remove

---

## ✅ Validação rápida do MVP
1. Suba o backend.
2. Faça login com `emilys / emilyspass`.
3. Use o frontend para CRUD, progresso e reordenação.
