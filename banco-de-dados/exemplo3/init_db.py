import sqlite3

def init_db():
    with sqlite3.connect('usuarios.db') as conn:
        cursor = conn.cursor()

        with open('db/database.sql', 'r') as f:
            sql_script = f.read()

        cursor.executescript(sql_script)
        conn.commit()
        print("Banco de dados inicializado com sucesso.")

if __name__ == '__main__':
    init_db()
