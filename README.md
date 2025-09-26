# naFilaPlus — Backend (Flask)

API em Flask com SQLite e CORS. Suporta autenticação externa **ReqRes** (padrão) ou **DummyJSON** e um **bypass** opcional para desenvolvimento.

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
docker run -d --name nafila-backend -p 5000:5000   -e EXTERNAL_AUTH_MODE=dummyjson   nafila-backend
```

Teste rápido:
```bash
curl -s http://127.0.0.1:5000/health
curl -s -X POST http://127.0.0.1:5000/auth/login   -H 'Content-Type: application/json'   -d '{"email":"emilys","password":"emilyspass"}'
```

## ▶️ Execução alternativa — **ReqRes** (padrão)
Credenciais de demonstração do serviço:
- **e‑mail:** `eve.holt@reqres.in`
- **senha:** `cityslicka`

```bash
docker rm -f nafila-backend 2>/dev/null || true
docker run -d --name nafila-backend -p 5000:5000 nafila-backend
```

> ⚠️ Observação: o endpoint público do ReqRes pode retornar `401` dependendo de políticas do serviço. Para a avaliação do MVP, prefira **DummyJSON** (instruções acima).

---

## 🔌 Variáveis de ambiente
- `EXTERNAL_AUTH_MODE` — `reqres` (default) ou `dummyjson`
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
- `POST /contents` → cria conteúdo
- `PUT /contents/:id` → atualiza
- `DELETE /contents/:id` → remove

---

## ✅ Validação rápida do MVP
1. Suba o backend (DummyJSON recomendado).
2. Faça login com `emilys / emilyspass`.
3. Use o frontend para CRUD e verificar progresso/drag‑and‑drop.
