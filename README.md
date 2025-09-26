# naFilaPlus — Backend (Flask)

API em Flask com SQLite e CORS. Suporta autenticação externa (ReqRes por padrão) e **bypass** para testes.

## Como rodar (Docker)
```bash
docker rm -f nafila-backend 2>/dev/null || true
docker build -t nafila-backend .
# (A) Execução cumprindo requisito de autenticação externa (ReqRes)
docker run -d --name nafila-backend -p 5000:5000 nafila-backend
# ou usando variáveis de ambiente por arquivo:
# cp .env.example .env  # edite se desejar
# docker run -d --name nafila-backend -p 5000:5000 --env-file .env nafila-backend

# (B) Modo teste local sem acessar API externa (somente para desenvolvimento)
# docker run -d --name nafila-backend -p 5000:5000 -e BYPASS_EXTERNAL_AUTH=1 nafila-backend
```

## Endpoints
- `GET /health` → `{"status":"ok"}`
- `POST /auth/login` → Autentica via API externa (ou bypass se habilitado)
- `GET/POST/PUT/DELETE /contents` → CRUD de conteúdos

## Autenticação Externa
- **URL padrão**: `https://reqres.in/api/login`
- **Credenciais de demonstração** (para o avaliador):
  - **E-mail:** `eve.holt@reqres.in`
  - **Senha:** `cityslicka`

> Essas credenciais são públicas do serviço **ReqRes** (somente para testes do MVP).

## Variáveis de ambiente
- `BYPASS_EXTERNAL_AUTH=1` → ignora API externa (qualquer email/senha funcionam) **somente testes**
- `EXTERNAL_AUTH_API_KEY=demo123` → exige header `x-api-key: demo123` no `/auth/login` (opcional)
- `EXTERNAL_AUTH_URL=https://reqres.in/api/login` → troca a URL da API externa (opcional)

### Via `--env-file`
Crie um `.env` a partir do `.env.example` e rode:
```bash
docker run -d --name nafila-backend -p 5000:5000 --env-file .env nafila-backend
```

## Teste rápido
```bash
curl -s http://localhost:5000/health
curl -s -X POST http://localhost:5000/auth/login   -H 'Content-Type: application/json'   -d '{"email":"eve.holt@reqres.in","password":"cityslicka"}'
# Se usar API key:
#   -H 'x-api-key: demo123'
```
