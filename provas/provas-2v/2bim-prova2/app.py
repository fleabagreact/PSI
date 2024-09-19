from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'ROMERITO_CAMPOS_E_A_NOSSA_VOZ'

login_manager = LoginManager()
login_manager.init_app(app)

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['matricula'], user['email'], user['senha'])
    return None

class User(UserMixin):
    def __init__(self, id, matricula, email, senha):
        self.id = id
        self.matricula = matricula
        self.email = email
        self.senha = senha

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not matricula or not email or not senha:
            flash('Todos os campos são obrigatórios!')
            return redirect(url_for('cadastro'))

        senha_hash = generate_password_hash(senha, method='pbkdf2:sha256')
        email_hash = generate_password_hash(email, method='pbkdf2:sha256')

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO usuarios (matricula, email, senha) VALUES (?, ?, ?)',
                         (matricula, email_hash, senha_hash))
            conn.commit()
            
            user = conn.execute('SELECT * FROM usuarios WHERE matricula = ?', (matricula,)).fetchone()
            login_user(User(user['id'], user['matricula'], user['email'], user['senha']))
        except sqlite3.IntegrityError:
            flash('Erro ao realizar o cadastro. Verifique se a matrícula ou e-mail já estão em uso.')
            return redirect(url_for('cadastro'))
        finally:
            conn.close()

        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('index'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        email = request.form.get('email')
        senha = request.form.get('senha')

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE matricula = ?', (matricula,)).fetchone()
        conn.close()

        if user and check_password_hash(user['senha'], senha) and check_password_hash(user['email'], email):
            login_user(User(user['id'], user['matricula'], user['email'], user['senha']))
            return redirect(url_for('index'))
        else:
            flash('Login inválido. Verifique suas credenciais.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.')
    return redirect(url_for('index'))

@app.route('/exercicio', methods=['GET', 'POST'])
@login_required
def exercicio():
    conn = get_db_connection()

    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        usuario_id = current_user.id

        conn.execute('INSERT INTO exercicios (nome, descricao, usuario_id) VALUES (?, ?, ?)',
                     (nome, descricao, usuario_id))
        conn.commit()
        flash('Exercício cadastrado com sucesso!')

    exercicios = conn.execute('SELECT * FROM exercicios WHERE usuario_id = ?', (current_user.id,)).fetchall()
    conn.close()

    return render_template('exercicios.html', exercicios=exercicios)

if __name__ == '__main__':
    app.run(debug=True)