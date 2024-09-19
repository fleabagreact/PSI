import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    with open('./db/schema.sql') as f:
        conn.executescript(f.read())
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado.")