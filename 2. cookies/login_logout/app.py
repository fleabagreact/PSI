from flask import Flask, request, render_template, url_for, session, redirect

app = Flask (__name__)

bancodedados = {}

app.config ['SECRET KEY'] = 'superdificil'

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/dashboard')
def dash():
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        if nome in bancodedados and bancodedados[nome] == senha:
            session['user'] = nome
            return redirect(url_for('dash'))
        else:
            return "Usuário inexistente ou senha incorreta"
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'user' in session:
        return redirect(url_for('dash'))

    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        if nome not in bancodedados:
            bancodedados[nome] = senha
            session['user'] = nome
            return redirect(url_for('dash'))
        else:
            return "Você já está cadastrado!"
        
    return render_template('register.html')

@app.route('/logout', method=['POST','GET'])
def logout():
    session.pop('user', None)
    redirect(url_for('index.html'))