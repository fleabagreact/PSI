from flask import Flask, render_template, request, redirect, url_for, session, make_response

app = Flask(__name__)
app.secret_key = 'luiza & naju'

@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username)
    return render_template('home.html', username=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'sylviephillia' and password == '#Gardensong16':
            session['username'] = username
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('username', username)
            return resp
        else:
            return render_template('login.html', error='Credenciais inválidas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('username', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(debug=True)
