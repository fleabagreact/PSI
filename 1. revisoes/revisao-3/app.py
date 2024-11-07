from flask import Flask, render_template, request, redirect, url_for, flash
from models import salvar_usuario, listar_usuarios

app = Flask(__name__)
app.secret_key = 'wanda_mae_de_the_sims'

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if not nome or not email or not senha:
            flash('Todos os campos são obrigatórios!')
        else:
            salvar_usuario(nome, email, senha)
            flash('Usuário cadastrado com sucesso!')
            return redirect(url_for('index'))
    
    return render_template('cadastro.html')

@app.route('/usuarios')
def usuarios():
    usuarios = listar_usuarios()
    return render_template('usuarios.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
