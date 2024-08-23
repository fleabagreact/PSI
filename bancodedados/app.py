from flask import Flask, request, render_template, url_for, redirect
import sqlite3

app = Flask(__name__)

# Obtém uma conexão com o banco de dados do SQLite
def get_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        conexao = get_connection()
        user = conexao.execute("SELECT * FROM users WHERE email = ? AND senha = ?", (nome, senha)).fetchone()
        conexao.close()

        if user:
            return redirect(url_for('dash'))
        else:
            return "Usuário inexistente ou senha incorreta"

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        conexao = get_connection()
        user = conexao.execute("SELECT * FROM users WHERE email = ?", (nome,)).fetchone()

        if user:
            conexao.close()
            return "Usuário já está cadastrado"
        else:
            conexao.execute("INSERT INTO users (email, senha) VALUES(?, ?)", (nome, senha))
            conexao.commit()
            conexao.close()
            return redirect(url_for('dash'))

    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)