from flask import Flask, render_template, jsonify, request, redirect, url_for, session, Response
import sqlite3
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Chemin ABSOLU vers la base SQLite (évite les "BDD vide" à cause du répertoire courant)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


# -------------------------
# Helpers DB / Auth
# -------------------------
def get_db():
    """Ouvre une connexion SQLite vers la base."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def require_user_auth_db():
    """
    Basic Auth: vérifie user/12345 dans la table users avec role='user'.
    Retourne user_id si OK, sinon une Response 401.
    """
    auth = request.authorization
    if not auth:
        return Response("Auth requise", 401, {"WWW-Authenticate": 'Basic realm="User Area"'})

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, role FROM users WHERE username=? AND password=?",
        (auth.username, auth.password),
    )
    row = cur.fetchone()
    conn.close()

    if not row or row["role"] != "user":
        return Response("Accès refusé (user)", 401, {"WWW-Authenticate": 'Basic realm="User Area"'})

    return row["id"]


def est_authentifie():
    """Vérifie si la session admin est authentifiée via /authentification."""
    return session.get("authentifie")


def require_admin_session():
    """Accès admin basé sur la session (admin/password via formulaire)."""
    if not est_authentifie():
        return Response("Accès refusé (admin requis)", 403)
    return None


# -------------------------
# Pages (TP initial)
# -------------------------
@app.route("/")
def hello_world():
    return render_template("hello.html")


@app.route("/lecture")
def lecture():
    if not est_authentifie():
        return redirect(url_for("authentification"))
    return "<h2>Bravo, vous êtes authentifié</h2>"


@app.route("/authentification", methods=["GET", "POST"])
def authentification():
    if request.method == "POST":
        if request.form.get("username") == "admin" and request.form.get("password") == "password":
            session["authentifie"] = True
            return redirect(url_for("lecture"))
        return render_template("formulaire_authentification.html", error=True)

    return render_template("formulaire_authentification.html", error=False)


# -------------------------
# Anciennes routes "clients" : neutralisées
# -------------------------
@app.route("/fiche_client/<int:post_id>")
def Readfiche(post_id):
    return "<h3>Ancienne route (clients) - utilise /api/books</h3>", 200


@app.route("/consultation/")
def ReadBDD():
    return redirect(url_for("api_books"))


# -------------------------
# API Bibliothèque
# -------------------------
@app.route("/api/books", methods=["GET"])
def api_books():
    user_id_or_denied = require_user_auth_db()
    if isinstance(user_id_or_denied, Response):
        return user_id_or_denied

    search = request.args.get("search", "").strip()

    conn = get_db()
    cur = conn.cursor()

    if search:
        cur.execute(
            """
            SELECT id, title, author, isbn, stock_total, stock_available
            FROM books
            WHERE stock_available > 0
              AND (title LIKE ? OR author LIKE ? OR isbn LIKE ?)
            ORDER BY title
            """,
            (f"%{search}%", f"%{search}%", f"%{search}%"),
        )
    else:
        cur.execute(
            """
            SELECT id, title, author, isbn, stock_total, stock_available
            FROM books
            WHERE stock_available > 0
            ORDER BY title
            """
        )

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)


@app.route("/api/borrow/<int:book_id>", methods=["POST"])
def api_borrow(book_id):
    user_id_or_denied = require_user_auth_db()
    if isinstance(user_id_or_denied, Response):
        return user_id_or_denied
    user_id = user_id_or_denied

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT stock_available FROM books WHERE id=?", (book_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Livre introuvable"}), 404

    if row["stock_available"] <= 0:
        conn.close()
        return jsonify({"error": "Plus de stock disponible"}), 409

    cur.execute(
        "INSERT INTO loans (user_id, book_id, loan_date, return_date) VALUES (?, ?, datetime('now'), NULL)",
        (user_id, book_id),
    )
    cur.execute("UPDATE books SET stock_available = stock_available - 1 WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "borrowed", "book_id": book_id, "user_id": user_id})


@app.route("/api/return/<int:book_id>", methods=["POST"])
def api_return(book_id):
    user_id_or_denied = require_user_auth_db()
    if isinstance(user_id_or_denied, Response):
        return user_id_or_denied
    user_id = user_id_or_denied

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id FROM loans
        WHERE user_id=? AND book_id=? AND return_date IS NULL
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id, book_id),
    )
    loan = cur.fetchone()

    if not loan:
        conn.close()
        return jsonify({"error": "Aucun emprunt actif trouvé"}), 404

    cur.execute("UPDATE loans SET return_date = datetime('now') WHERE id=?", (loan["id"],))
    cur.execute("UPDATE books SET stock_available = stock_available + 1 WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "returned", "book_id": book_id, "user_id": user_id})


# -------------------------
# Admin (session)
# -------------------------
@app.route("/api/admin/books", methods=["POST"])
def admin_add_book():
    denied = require_admin_session()
    if denied:
        return denied

    data = request.get_json(force=True)
    title = (data.get("title") or "").strip()
    author = (data.get("author") or "").strip()
    isbn = data.get("isbn")
    stock_total = int(data.get("stock_total", 1))

    if not title or not author or stock_total < 1:
        return jsonify({"error": "title/author/stock_total invalides"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO books (title, author, isbn, stock_total, stock_available)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, author, isbn, stock_total, stock_total),
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "book_added"})


@app.route("/api/admin/books/<int:book_id>", methods=["DELETE"])
def admin_delete_book(book_id):
    denied = require_admin_session()
    if denied:
        return denied

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "book_deleted", "book_id": book_id})


@app.route("/admin")
def admin_home():
    if not est_authentifie():
        return redirect(url_for("authentification"))
    return """
    <h2>Admin Library</h2>
    <p>Tu es admin ✅</p>
    <ul>
      <li>POST /api/admin/books (JSON)</li>
      <li>DELETE /api/admin/books/&lt;id&gt;</li>
    </ul>
    """


# -------------------------
# Debug preuve "BDD non vide"
# -------------------------
@app.route("/api/debug/counts")
def debug_counts():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS c FROM books")
    books = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) AS c FROM users")
    users = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) AS c FROM loans")
    loans = cur.fetchone()["c"]
    conn.close()
    return jsonify({"books": books, "users": users, "loans": loans})
