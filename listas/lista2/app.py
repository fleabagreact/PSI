from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return "Esta é a página Sobre."

@app.route('/perfil/<nome>')
def perfil(nome):
    if nome.lower() == "anônimo":
        return redirect(url_for('home'))
    return f"Olá, {nome}! Bem-vindo ao seu perfil."

if __name__ == '__main__':
    app.run(debug=True)
