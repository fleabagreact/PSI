from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bem-vindo(a)"

@app.route('/sobre')
def sobre():
    return "Esta é a página Sobre"

@app.route('/saudacao/<nome>')
def saudacao(nome):
    return f"Olá, {nome}! Bem-vindo(a) ao Flask!"

@app.route('/contato')
def contato():
    return "Contato: Esta é uma página fictícia de contato!"

if __name__ == '__main__':
    app.run(debug=True)
