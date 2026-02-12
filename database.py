import sqlite3

def setup_db():
    conn = sqlite3.connect('marches.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS annonces (
            id TEXT PRIMARY KEY,
            titre TEXT,
            resume TEXT,
            lien TEXT,
            date_decouverte DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_annonce(id, titre, resume, lien):
    conn = sqlite3.connect('marches.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO annonces (id, titre, resume, lien) VALUES (?, ?, ?, ?)', 
                       (id, titre, resume, lien))
        conn.commit()
    except:
        pass # Déjà présent en base, on ne fait rien
    conn.close()

def get_all_annonces():
    conn = sqlite3.connect('marches.db')
    cursor = conn.cursor()
    cursor.execute('SELECT titre, resume, lien, date_decouverte FROM annonces ORDER BY date_decouverte DESC')
    data = cursor.fetchall()
    conn.close()
    return data