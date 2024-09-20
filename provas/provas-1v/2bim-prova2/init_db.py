import sqlite3

conn = sqlite3.connect('database.db')

with open('db/schema.sql', 'r') as f:
    conn.executescript(f.read())

conn.close()

print("Banco de dados inicializado!")
