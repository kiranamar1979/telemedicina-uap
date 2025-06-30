
from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
from weasyprint import HTML
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'
DB = 'medica.db'

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['usuario']
        pwd = request.form['password']
        if user == 'medico@uap.com' and pwd == 'admin123':
            session['user'] = user
            return redirect('/dashboard')
        return render_template('login.html', error='Credenciales inválidas')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM citas")
    citas = cur.fetchall()
    return render_template("dashboard.html", citas=citas)

@app.route('/historia', methods=['GET', 'POST'])
def historia():
    if request.method == 'POST':
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        edad = request.form['edad']
        anamnesis = request.form['anamnesis']
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']
        estudios = request.form['estudios']
        presion = request.form['presion']
        talla = request.form['talla']
        peso = request.form['peso']

        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("INSERT INTO historias (fecha, nombre, edad, anamnesis, diagnostico, tratamiento, estudios, presion, talla, peso) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (fecha, nombre, edad, anamnesis, diagnostico, tratamiento, estudios, presion, talla, peso))
        con.commit()
        con.close()

        rendered = render_template('historia_pdf.html', fecha=fecha, nombre=nombre, edad=edad,
                                   anamnesis=anamnesis, diagnostico=diagnostico, tratamiento=tratamiento,
                                   estudios=estudios, presion=presion, talla=talla, peso=peso)

        pdf_filename = f"historia_{nombre.replace(' ', '_')}_{fecha}.pdf"
        HTML(string=rendered).write_pdf(pdf_filename)
        return send_file(pdf_filename, as_attachment=True)

    return render_template('historia.html')

@app.route('/descargar_historia')
def descargar_historia():
    datos = {
        'fecha': '2025-06-30',
        'nombre': 'Paciente Ejemplo',
        'edad': '35',
        'anamnesis': 'Dolor de cabeza frecuente.',
        'diagnostico': 'Migraña crónica',
        'tratamiento': 'Paracetamol 500mg cada 8h',
        'estudios': 'Tomografía cerebral',
        'presion': '120/80',
        'talla': '170',
        'peso': '70'
    }
    rendered = render_template('historia_pdf.html', **datos)
    pdf_path = os.path.join('static', 'historia.pdf')
    HTML(string=rendered).write_pdf(pdf_path)
    return send_file(pdf_path, as_attachment=True)

@app.route('/reporte', methods=['GET', 'POST'])
def reporte():
    historias = []
    fecha = None
    if request.method == 'POST':
        fecha = request.form['fecha']
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("SELECT * FROM historias WHERE fecha = ?", (fecha,))
        historias = cur.fetchall()
        con.close()
    return render_template('reporte.html', historias=historias, fecha=fecha)

def init_db():
    if not os.path.exists(DB):
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.executescript("""
CREATE TABLE IF NOT EXISTS citas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente TEXT,
    fecha TEXT,
    hora TEXT,
    especialidad TEXT
);

CREATE TABLE IF NOT EXISTS historias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    nombre TEXT,
    edad INTEGER,
    anamnesis TEXT,
    diagnostico TEXT,
    tratamiento TEXT,
    estudios TEXT,
    presion TEXT,
    talla TEXT,
    peso TEXT
);
""")
        con.commit()
        con.close()

init_db()

if __name__ == '__main__':
    app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))  # Usa el puerto que Render define
    app.run(host='0.0.0.0', port=port, debug=True)
