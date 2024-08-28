from flask import Flask, request, make_response, render_template, redirect, url_for

app = Flask(__name__)
resultados = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        resp = make_response(redirect(url_for('resultado')))
        resp.set_cookie('username', username)
        return resp
    return render_template('login.html')

@app.route('/corrida', methods=['GET', 'POST'])
def resultado():
    username = request.cookies.get('username')
    if request.method == 'POST':
        distancia = request.form['distancia']
        tempo = request.form['tempo']
        resultados.append({'user': username, 'distancia': distancia, 'tempo':tempo})
    user_resultados = [m for m in resultados if m['user'] == username]
    return render_template('corrida.html', lista_resultado_distancia=user_resultados, username=username)

if __name__ == '__main__':
    app.run(debug=True)