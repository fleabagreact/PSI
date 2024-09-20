from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from models import Usuario, create_tecnologia, get_tecnologias

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LOVE_IS_A_DAGGER'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Carregar o usuário pelo ID
@login_manager.user_loader
def load_user(user_id):
    user = Usuario.get_by_id(user_id)
    if user:
        return Usuario(user['id'], user['email'], user['cpf'], user['senha'], user['tipo'])
    return None

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Cadastro de usuário
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form['email']
        cpf = request.form['cpf']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']
        tipo = request.form['tipo']
        
        if senha == confirmar_senha:
            Usuario.create(email, cpf, senha, tipo)
            user = Usuario.get_by_email(email)
            usuario = Usuario(user['id'], user['email'], user['cpf'], user['senha'], user['tipo'])
            login_user(usuario)
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Senhas não conferem', 'danger')
    return render_template('cadastro.html')

# Login de usuário
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = Usuario.get_by_email(email)
        if user and check_password_hash(user['senha'], senha):
            usuario = Usuario(user['id'], user['email'], user['cpf'], user['senha'], user['tipo'])
            login_user(usuario)
            flash(f'Bem-vindo, {user["email"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login ou senha incorretos', 'danger')
    return render_template('login.html')

# Logout de usuário
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('index'))

# Página de dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    tecnologias = get_tecnologias()
    return render_template('dashboard.html', tecnologias=tecnologias)

# Cadastro de tecnologia (ADMIN)
@app.route('/cadastro_tecnologia', methods=['GET', 'POST'])
@login_required
def cadastro_tecnologia():
    if current_user.tipo != 'ADMIN':
        flash('Acesso negado. Apenas ADMINs podem cadastrar tecnologias.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        sigla = request.form['sigla']
        descricao = request.form['descricao']
        create_tecnologia(nome, sigla, descricao)
        flash('Tecnologia cadastrada com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('cadastro_tecnologia.html')

if __name__ == '__main__':
    app.run(debug=True)