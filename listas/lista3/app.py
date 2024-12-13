from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/formulario', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        comentario = request.form.get('comentario')
        return f"""
        <h1>Obrigado pelo feedback, {nome}!</h1>
        <p>Email: {email}</p>
        <p>Comentário recebido: {comentario}</p>
        """
    return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)

