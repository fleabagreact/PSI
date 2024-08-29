from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def get_theme():
    return request.cookies.get('theme', 'light')

@app.route('/')
def index():
    username = request.cookies.get('username')
    theme = get_theme()
    return render_template('index.html', username=username, theme=theme)

@app.route('/register', methods=['GET', 'POST'])
def register():
    theme = get_theme()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        theme = request.form['theme']

        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO users (username, password, theme) VALUES (?, ?, ?)', (username, password, theme))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Nome de usuário já existe"
        finally:
            conn.close()

        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('username', username)
        resp.set_cookie('theme', theme)
        return resp

    return render_template('register.html', theme=theme)

@app.route('/login', methods=['GET', 'POST'])
def login():
    theme = get_theme()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            theme = user[3]
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('username', username)
            resp.set_cookie('theme', theme)
            return resp
        else:
            return "Nome de usuário ou senha incorretos"
    return render_template('login.html', theme=theme)

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('theme', 'light')
    return resp

@app.route('/toggle-theme')
def toggle_theme():
    theme = get_theme()
    new_theme = 'dark' if theme == 'light' else 'light'
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('theme', new_theme)
    return resp

if __name__ == '__main__':
    app.run(debug=True)