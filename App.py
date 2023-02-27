from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#conexion mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'prestamo'
mysql = MySQL(app)

#configuraciones
app.secret_key = 'WKv&bB9w^*9fW%HjojCZ%8vUnxg6'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data) 

@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    if request.method == 'POST':
        numempleado = request.form['numempleado']
        usuario = request.form['usuario']
        accesorio = request.form['accesorio']
        descripcion = request.form['descripcion']
        fecha = request.form['fechaR']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (numempleado, usuario, accesorio, descripcion, fechaR) VALUES (%s, %s, %s, %s, %s)', (numempleado, usuario, accesorio, descripcion, fecha))
        mysql.connection.commit()
        flash('Prestamo Realizado Exitosamente')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_equipment(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit-equipment.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_equipmentt(id):
    if request.method == 'POST':
        fechaR = request.form['fechaR']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contacts SET fechaR = %s WHERE id = %s', (fechaR, id))
        mysql.connection.commit()
        flash('Fecha de Retorno Cambiado')
        return redirect(url_for('Index'))

@app.route('/reporte')
def reporte():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('reporte.html', contacts = data) 
    
@app.route('/delete/<string:id>')
def delete_equipment(id):
    status = 1
    cur = mysql.connection.cursor()
    cur.execute('UPDATE contacts SET status = %s where id = %s',(status, id))
    mysql.connection.commit()
    flash('Prestamo Retornado Exitosamente')
    return redirect(url_for('Index'))

@app.route('/add-equipment')
def addequipment():
    return render_template('add-equipment.html')

if __name__ == '__main__':
    app.run(port = 3000, debug = True)
