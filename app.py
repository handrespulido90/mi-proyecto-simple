from flask import Flask, render_template, request, redirect
import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Obtener la URL de la base de datos desde .env
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Conecta a la base de datos PostgreSQL en Render"""
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    return conn

def init_db():
    """Crea la tabla si no existe"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Página principal con lista de usuarios"""
    conn = get_db_connection()
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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES (%s, %s)", (nombre, edad))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()  # Asegurar que la tabla exista antes de iniciar la aplicación
    app.run(debug=True)