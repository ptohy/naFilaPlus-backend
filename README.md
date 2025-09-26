# naFilaPlus — Backend (Flask)

API em Flask com SQLite e CORS. Suporta autenticação externa **DummyJSON** (recomendado) ou **ReqRes** e possui **bypass** opcional para desenvolvimento.

---

## 🔧 Pré‑requisitos
- Docker

---

## 🚀 Build
```bash
docker rm -f nafila-backend 2>/dev/null || true
docker build -t nafila-backend .
```

## ▶️ Execução (recomendado para avaliação) — **DummyJSON**
O DummyJSON usa **username** no lugar de e‑mail. Credenciais públicas e estáveis:
- **username:** `emilys`
- **password:** `emilyspass`

```bash
docker run -d --name nafila-backend -p 5000:5000 \
  -e EXTERNAL_AUTH_MODE=dummyjson \
  nafila-backend
```

Teste rápido:
```bash
curl -s http://127.0.0.1:5000/health
curl -s -X POST http://127.0.0.1:5000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"emilys","password":"emilyspass"}'
# -> 200 OK + {"message":"Login bem-sucedido","token":"..."}
```

> ℹ️ Se preferir **ReqRes** (usa *e‑mail*), rode sem `EXTERNAL_AUTH_MODE` ou defina `EXTERNAL_AUTH_MODE=reqres`. Atenção: o endpoint público do ReqRes pode responder `401` dependendo de políticas do serviço; para a avaliação do MVP, prefira **DummyJSON**.

---

## 🔌 Variáveis de ambiente
- `EXTERNAL_AUTH_MODE` — `dummyjson` (recomendado) ou `reqres` (padrão se não definido)
- `EXTERNAL_AUTH_URL` — sobrescreve a URL do provedor externo (opcional)
- `BYPASS_EXTERNAL_AUTH=1` — ativa login fake (`token: dev-local`) **apenas para DEV**

Exemplo via `--env-file`:
```bash
docker run -d --name nafila-backend -p 5000:5000 --env-file .env nafila-backend
```

---

## 📚 Endpoints
- `GET /health` → `{"status":"ok"}`
- `POST /auth/login` → autentica no provedor externo (ou bypass, se habilitado)
- `GET /contents` → lista conteúdos (filtros opcionais `?status=&tipo=`)
- `POST /contents` → cria conteúdo (progresso inicial = 0)
- `PUT /contents/:id` → atualiza
- `DELETE /contents/:id` → remove

---

## ✅ Roteiro de validação do MVP
1. Suba o backend **em DummyJSON** (comando acima).
2. Faça login com `emilys / emilyspass` pelo frontend.
3. Execute o CRUD, use “Concluir” e reordene com **drag‑and‑drop** (ordem persiste no navegador).
