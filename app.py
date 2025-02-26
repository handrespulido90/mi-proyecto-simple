from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    """Inicializa la base de datos"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        edad INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Página principal con lista de usuarios"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return render_template('index.html', usuarios=usuarios)

@app.route('/agregar', methods=['POST'])
def agregar_usuario():
    """Agrega un usuario a la base de datos"""
    nombre = request.form['nombre']
    edad = request.form['edad']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES (?, ?)", (nombre, edad))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
