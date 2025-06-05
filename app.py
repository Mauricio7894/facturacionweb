from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import pandas as pd
from datetime import datetime
import os

# Crear instancia de Flask
app = Flask(__name__)

# Crear base de datos si no existe
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
            anio INTEGER,
            monto REAL
        )
    ''')
    conn.commit()
    conn.close()

# Ejecutar creación de base de datos
init_db()

# Página de Inicio
@app.route('/')
def home():
    return render_template('home.html')
# Página principal (Formulario)
@app.route('/')
def index():
    return render_template('form.html')

# Guardar datos que llenamos en el formulario
@app.route('/guardar', methods=['POST'])
def guardar():
    iata = request.form['iata'].upper()
    agt = request.form['agt'].upper()
    negocio = request.form['negocio'].upper()
    registro = request.form['registro']
    mes = int(request.form['mes'])
    anio = int(request.form['anio'])
    monto = float(request.form['monto'])

    # Si es factura, monto en negativo
    if registro == "Factura":
        monto = -abs(monto)
    else:
        monto = abs(monto)

    conn = sqlite3.connect('facturacion_web.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO facturacion (iata, agt, negocio, registro, mes, anio, monto)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (iata, agt, negocio, registro, mes, anio, monto))
    conn.commit()
    conn.close()

    return redirect('/')

# Exportar los datos a Excel
@app.route('/exportar')
def exportar():
    conn = sqlite3.connect('facturacion_web.db')
    df = pd.read_sql_query('SELECT * FROM facturacion', conn)
    conn.close()

    if df.empty:
        return "No hay datos para exportar."

    fecha_hoy = datetime.today().strftime('%Y-%m-%d')
    filename = f'reporte_facturacion_{fecha_hoy}.xlsx'
    df.to_excel(filename, index=False)

    return send_file(filename, as_attachment=True)

# Ejecutar app
if __name__ == '__main__':
    app.run(debug=True)
