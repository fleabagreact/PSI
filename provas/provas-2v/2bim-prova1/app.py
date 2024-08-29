from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'escola.db'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT)')
    
    cursor.execute('SELECT nome, email FROM usuarios')
    usuarios = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html', usuarios=usuarios)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO usuarios (nome, email) VALUES (?, ?)', (nome, email))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('cadastrar.html')

if __name__ == '__main__':
    app.run(debug=True)