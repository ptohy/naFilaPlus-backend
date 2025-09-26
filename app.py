from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, requests, os

app = Flask(__name__)
CORS(app)

DB_NAME = "nafila.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS contents
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      tipo TEXT NOT NULL,
                      status TEXT NOT NULL,
                      progresso INTEGER DEFAULT 0)''')
        conn.commit()

def get_db_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

init_db()

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()      # <- aqui pode ser "username" (DummyJSON usa username)
    password = (data.get("password") or "").strip()
    if not email or not password:
        return jsonify({"error": "Email/usuário e senha são obrigatórios"}), 400

    # BYPASS opcional (apenas DEV)
    if (os.getenv("BYPASS_EXTERNAL_AUTH") or "").strip() == "1":
        return jsonify({"message": "Login bem-sucedido", "token": "dev-local"}), 200

    # 🔒 ReqRes DESATIVADO. Somente DummyJSON:
    # - username: emilys
    # - password: emilyspass
    auth_url = (os.getenv("EXTERNAL_AUTH_URL") or "https://dummyjson.com/auth/login").strip()
    payload = {"username": email, "password": password}

    try:
        r = requests.post(auth_url, json=payload, timeout=10)
        if r.status_code >= 400:
            # DummyJSON retorna {"message":"Invalid credentials"} para credenciais erradas
            try:
                body = r.json()
            except Exception:
                body = {"status_code": r.status_code, "body": r.text[:200]}
            return jsonify({"error": "Falha no login externo", "details": body}), 401
        token = r.json().get("token") or "external-ok"
        return jsonify({"message": "Login bem-sucedido", "token": token}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Falha no login externo", "details": {"error": str(e)}}), 401

# -------- CRUD --------
@app.route("/contents", methods=["GET"])
def get_contents():
    status = request.args.get("status")
    tipo = request.args.get("tipo")
    query = "SELECT * FROM contents WHERE 1=1"
    params = []
    if status:
        query += " AND status=?"
        params.append(status)
    if tipo:
        query += " AND tipo=?"
        params.append(tipo)
    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute(query, params)
        rows = c.fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/contents", methods=["POST"])
def add_content():
    data = request.get_json(silent=True) or {}
    for f in ["title", "tipo", "status"]:
        if not data.get(f):
            return jsonify({"error": f"Campo obrigatório ausente: {f}"}), 400
    title = data["title"]
    tipo = data["tipo"]
    status = data["status"]
    # Sempre 0 no cadastro inicial
    progresso = 0

    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO contents (title, tipo, status, progresso) VALUES (?, ?, ?, ?)",
                  (title, tipo, status, progresso))
        conn.commit()
        new_id = c.lastrowid
    return jsonify({"id": new_id}), 201

@app.route("/contents/<int:content_id>", methods=["PUT"])
def update_content(content_id):
    data = request.get_json(silent=True) or {}
    for f in ["title", "tipo", "status"]:
        if not data.get(f):
            return jsonify({"error": f"Campo obrigatório ausente: {f}"}), 400
    title = data["title"]
    tipo = data["tipo"]
    status = data["status"]
    progresso = int(data.get("progresso", 0) or 0)
    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute("UPDATE contents SET title=?, tipo=?, status=?, progresso=? WHERE id=?",
                  (title, tipo, status, progresso, content_id))
        conn.commit()
        if c.rowcount == 0:
            return jsonify({"error": "Conteúdo não encontrado"}), 404
    return jsonify({"message": "Atualizado com sucesso"})

@app.route("/contents/<int:content_id>", methods=["DELETE"])
def delete_content(content_id):
    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM contents WHERE id=?", (content_id,))
        conn.commit()
        if c.rowcount == 0:
            return jsonify({"error": "Conteúdo não encontrado"}), 404
    return jsonify({"message": "Deletado com sucesso"})

if __name__ == "__main__":
    # Flask rodando em 0.0.0.0 para o container expor a porta
    app.run(host="0.0.0.0", port=5000, debug=False)
