from werkzeug.security import generate_password_hash
import sqlite3
from flask_login import UserMixin

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

class Usuario(UserMixin):
    def __init__(self, id, email, cpf, senha, tipo):
        self.id = id
        self.email = email
        self.cpf = cpf
        self.senha = senha
        self.tipo = tipo

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        conn.close()
        return user

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return user

    @staticmethod
    def create(email, cpf, senha, tipo):
        hashed_cpf = generate_password_hash(cpf)
        hashed_senha = generate_password_hash(senha) 
        conn = get_db_connection()
        conn.execute('INSERT INTO usuarios (email, cpf, senha, tipo) VALUES (?, ?, ?, ?)',
                     (email, hashed_cpf, hashed_senha, tipo))
        conn.commit()
        conn.close()

def create_tecnologia(nome, sigla, descricao):
    conn = get_db_connection()
    conn.execute('INSERT INTO tecnologias (nome, sigla, descricao) VALUES (?, ?, ?)',
                 (nome, sigla, descricao))
    conn.commit()
    conn.close()

def get_tecnologias():
    conn = get_db_connection()
    tecnologias = conn.execute('SELECT * FROM tecnologias').fetchall()
    conn.close()
    return tecnologias