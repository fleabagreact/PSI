from flask import Flask, request, make_response, render_template, redirect, url_for

app = Flask(__name__)
mensagens = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        resp = make_response(redirect(url_for('mensagem')))
        resp.set_cookie('username', username)
        return resp
    return render_template('login.html')

@app.route('/mensagem', methods=['GET', 'POST'])
def mensagem():
    username = request.cookies.get('username')
    if request.method == 'POST':
        mensagem = request.form['mensagem']
        mensagens.append({'user': username, 'text': mensagem})
    user_mensagens = [m for m in mensagens if m['user'] == username]
    return render_template('mensagem.html', mensagens=user_mensagens, username=username)

if __name__ == '__main__':
    app.run(debug=True)