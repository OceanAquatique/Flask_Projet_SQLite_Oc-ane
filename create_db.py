import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('DUPONT', 'Emilie', '123, Rue des Lilas, 75001 Paris'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('LEROUX', 'Lucas', '456, Avenue du Soleil, 31000 Toulouse'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('MARTIN', 'Amandine', '789, Rue des Érables, 69002 Lyon'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('TREMBLAY', 'Antoine', '1010, Boulevard de la Mer, 13008 Marseille'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('LAMBERT', 'Sarah', '222, Avenue de la Liberté, 59000 Lille'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('GAGNON', 'Nicolas', '456, Boulevard des Cerisiers, 69003 Lyon'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('DUBOIS', 'Charlotte', '789, Rue des Roses, 13005 Marseille'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('LEFEVRE', 'Thomas', '333, Rue de la Paix, 75002 Paris'))

connection.commit()
connection.close()

import sqlite3

DB = "database.db"

def main():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Charge le schema.sql et l'exécute
    with open("schema.sql", "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    # Comptes par défaut
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", "password", "admin"))
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("user", "12345", "user"))

    # Livres de démo
    cursor.execute("INSERT INTO books (title, author, isbn, stock_total, stock_available) VALUES (?, ?, ?, ?, ?)",
                   ("1984", "George Orwell", "9780451524935", 3, 3))
    cursor.execute("INSERT INTO books (title, author, isbn, stock_total, stock_available) VALUES (?, ?, ?, ?, ?)",
                   ("Le Petit Prince", "Antoine de Saint-Exupéry", "9782070612758", 2, 2))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
