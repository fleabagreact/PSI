from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def index ():
    return "Rhaenyra, rainha legítima dos sete reinos"

@app.route('/render')
def render ():
    return render_template ('index.html')

@app.route('/dados')
def dados():
    nome = 'Rhaenyra, the realm delight'
    return render_template ('dados.html', nome=nome)

@app.route('/formulario', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template ('formulario.html')
    else:
        nome = request.form ['nome']
        return nome