from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Crear Base de Datos (por si no existe)
def init_db():
    conn = sqlite3.connect('facturacion_web.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            iata TEXT,
            agt TEXT,
            negocio TEXT,
            registro TEXT,
            mes INTEGER,
            año INTEGER,
            monto REAL
        )
    ''')
    conn.commit()
    conn.close()

# Página de Inicio 🚀
@app.route('/')
def home():
    return render_template('home.html')  # <--- esta es la página que carga el botón

# Página: Provisión Agentes (el formulario que ya tienes)
@app.route('/provision_agentes')
def provision_agentes():
    return render_template('provision_agentes.html')

# Ruta para guardar datos (cuando le das Guardar en el formulario)
@app.route('/guardar', methods=['POST'])
def guardar():
    # Tu código para guardar datos en SQLite
    iata = request.form['iata']
    agt = request.form['agt']
    negocio = request.form['negocio']
    registro = request.form['registro']
    mes = request.form['mes']
    año = request.form['año']
    monto = request.form['monto']

    conn = sqlite3.connect('facturacion_web.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO facturacion (iata, agt, negocio, registro, mes, año, monto) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                   (iata, agt, negocio, registro, mes, año, monto))
    conn.commit()
    conn.close()

    return redirect('/provision_agentes')  # Redirige después de guardar

# Ruta para exportar el reporte
@app.route('/exportar')
def exportar():
    conn = sqlite3.connect('facturacion_web.db')
    df = pd.read_sql_query('SELECT * FROM facturacion', conn)
    conn.close()

    output_file = f"reporte_facturacion_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    df.to_excel(output_file, index=False)

    return f"Reporte generado: {output_file}"

# Inicializar la base de datos
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
