from flask import Flask, session, request, render_template, url_for, redirect
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'superdificil'

def add_user(nome, senha):
    with sqlite3.connect('usuarios.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nome, senha) VALUES (?, ?)', (nome, senha))
        conn.commit()

def get_user(nome):
    with sqlite3.connect('usuarios.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE nome = ?', (nome,))
        return cursor.fetchone()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dash():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', nome=session['user'])

@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'user' in session:
        return redirect(url_for('dash'))

    if request.method == 'GET':
        return render_template('login.html')
    else:
        nome = request.form['nome']
        senha = request.form['senha']

        user = get_user(nome)
        if user and user[2] == senha:
            session['user'] = nome
            return redirect(url_for('dash'))
        else:
            return "SENHA INCORRETA ou não está cadastrado"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect(url_for('dash'))

    if request.method == 'GET':
        return render_template('register.html')
    else:
        nome = request.form['nome']
        senha = request.form['senha']

        user = get_user(nome)
        if not user:
            add_user(nome, senha)
            session['user'] = nome
            return redirect(url_for('dash'))
        else:
            return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    if 'user' in session:
        session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)