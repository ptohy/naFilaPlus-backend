from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__)
DB_NAME = "nafila.db"

# Inicialização do banco
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contents
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  tipo TEXT NOT NULL,
                  status TEXT NOT NULL,
                  progresso INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()

# -------- Rotas de Autenticação --------
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    # Chamada à API externa ReqRes
    r = requests.post("https://reqres.in/api/login", json=data)
    if r.status_code == 200:
        token = r.json().get("token")
        return jsonify({"message": "Login bem-sucedido", "token": token}), 200
    return jsonify({"error": "Falha no login"}), 401

# -------- CRUD de Conteúdos --------
@app.route("/contents", methods=["GET"])
def get_contents():
    status = request.args.get("status")
    tipo = request.args.get("tipo")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    query = "SELECT * FROM contents WHERE 1=1"
    params = []
    if status:
        query += " AND status=?"
        params.append(status)
    if tipo:
        query += " AND tipo=?"
        params.append(tipo)
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "title": r[1], "tipo": r[2], "status": r[3], "progresso": r[4]} for r in rows])

@app.route("/contents", methods=["POST"])
def add_content():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO contents (title, tipo, status, progresso) VALUES (?, ?, ?, ?)",
              (data["title"], data["tipo"], data["status"], data.get("progresso", 0)))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return jsonify({"id": new_id}), 201

@app.route("/contents/<int:content_id>", methods=["PUT"])
def update_content(content_id):
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE contents SET title=?, tipo=?, status=?, progresso=? WHERE id=?",
              (data["title"], data["tipo"], data["status"], data.get("progresso", 0), content_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Atualizado com sucesso"})

@app.route("/contents/<int:content_id>", methods=["DELETE"])
def delete_content(content_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM contents WHERE id=?", (content_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deletado com sucesso"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
