from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3
from flask import request, Response
imporyt os

USER_LOGIN = "user"
USER_PASSWORD = "12345"

def require_user_auth():
    # Vérifie une authentification Basic Auth user/12345.
    auth = request.authorization
    if not auth or not (auth.username == USER_LOGIN and auth.password == USER_PASSWORD):
        return Response(
            "Accès refusé (auth user requise)",
            401,
            {"WWW-Authenticate": 'Basic realm="User Area"'}
        )
    return None

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement

@app.route('/fiche_nom/', methods=['GET', 'POST'])
def fiche_nom():
    # Protection user/12345 (Basic Auth)
    deny = require_user_auth()
    if deny:
        return deny

    # Récupération du nom (POST via formulaire, ou GET via ?nom=)
    nom = ""
    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
    else:
        nom = request.args.get('nom', '').strip()

    # Si aucun nom fourni, afficher un petit formulaire
    if not nom:
        return """
        <h2>Recherche client par nom</h2>
        <form method="POST">
            <label>Nom :</label>
            <input name="nom" placeholder="Ex: DUPONT" required>
            <button type="submit">Rechercher</button>
        </form>
        <p>Astuce: tu peux aussi utiliser /fiche_nom/?nom=DUPONT</p>
        """

    # Recherche en base (LIKE pour accepter recherche partielle)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE nom LIKE ?', (f"%{nom}%",))
    data = cursor.fetchall()
    conn.close()

    # Réutilise ton template existant pour afficher la liste
    return render_template('read_data.html', data=data)

if __name__ == "__main__":
  app.run(debug=True)

def get_db():
    return sqlite3.connect(DB_PATH)

def require_user_auth_db():
    auth = request.authorization
    if not auth:
        return Response("Auth requise", 401, {"WWW-Authenticate": 'Basic realm="User Area"'})

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, role FROM users WHERE username=? AND password=?", (auth.username, auth.password))
    row = cur.fetchone()
    conn.close()

    if not row or row[1] != "user":
        return Response("Accès refusé", 401, {"WWW-Authenticate": 'Basic realm="User Area"'})

    # on renvoie l'user_id pour les emprunts
    return row[0]
def get_db():
    """Ouvre une connexion SQLite vers la base."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def require_user_auth_db():
    """Basic Auth: vérifie user/12345 dans la table users avec role=user.
       Retourne user_id si OK, sinon une Response 401."""
    auth = request.authorization
    if not auth:
        return Response("Auth requise", 401, {"WWW-Authenticate": 'Basic realm="User Area"'})

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, role FROM users WHERE username=? AND password=?", (auth.username, auth.password))
    row = cur.fetchone()
    conn.close()

    if not row or row["role"] != "user":
        return Response("Accès refusé (user)", 401, {"WWW-Authenticate": 'Basic realm="User Area"'})

    return row["id"]

def require_admin_session():
    """Vérifie que la session admin est authentifiée via /authentification."""
    if not est_authentifie():
        return Response("Accès refusé (admin requis)", 403)
    return None

@app.route("/api/books", methods=["GET"])
def api_books():
    user_id_or_denied = require_user_auth_db()
    if isinstance(user_id_or_denied, Response):
        return user_id_or_denied

    search = request.args.get("search", "").strip()

    conn = get_db()
    cur = conn.cursor()

    if search:
        cur.execute("""
            SELECT id, title, author, isbn, stock_total, stock_available
            FROM books
            WHERE stock_available > 0
              AND (title LIKE ? OR author LIKE ? OR isbn LIKE ?)
            ORDER BY title
        """, (f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        cur.execute("""
            SELECT id, title, author, isbn, stock_total, stock_available
            FROM books
            WHERE stock_available > 0
            ORDER BY title
        """)

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

    # Vérifie stock dispo
    cur.execute("SELECT stock_available FROM books WHERE id=?", (book_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Livre introuvable"}), 404

    if row["stock_available"] <= 0:
        conn.close()
        return jsonify({"error": "Plus de stock disponible"}), 409

    # Enregistre l'emprunt + décrémente stock
    cur.execute("INSERT INTO loans (user_id, book_id, loan_date, return_date) VALUES (?, ?, datetime('now'), NULL)",
                (user_id, book_id))
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

    # Trouve un emprunt actif de cet utilisateur sur ce livre
    cur.execute("""
        SELECT id FROM loans
        WHERE user_id=? AND book_id=? AND return_date IS NULL
        ORDER BY id DESC
        LIMIT 1
    """, (user_id, book_id))
    loan = cur.fetchone()

    if not loan:
        conn.close()
        return jsonify({"error": "Aucun emprunt actif trouvé"}), 404

    # Marque comme rendu + incrémente stock
    cur.execute("UPDATE loans SET return_date = datetime('now') WHERE id=?", (loan["id"],))
    cur.execute("UPDATE books SET stock_available = stock_available + 1 WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "returned", "book_id": book_id, "user_id": user_id})

@app.route("/api/admin/books", methods=["POST"])
def admin_add_book():
    denied = require_admin_session()
    if denied:
        return denied

    data = request.get_json(force=True)
    title = data.get("title", "").strip()
    author = data.get("author", "").strip()
    isbn = data.get("isbn")
    stock_total = int(data.get("stock_total", 1))

    if not title or not author or stock_total < 1:
        return jsonify({"error": "title/author/stock_total invalides"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO books (title, author, isbn, stock_total, stock_available)
        VALUES (?, ?, ?, ?, ?)
    """, (title, author, isbn, stock_total, stock_total))
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

