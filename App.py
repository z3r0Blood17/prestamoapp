from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import config
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from models.ModelUser import ModelUser
from models.entities.User import User

app = Flask(__name__)

app.secret_key = 'WKv&bB9w^*9fW%HjojCZ%8vUnxg6'
# conexion mysql
mysql = MySQL(app)

csrf = CSRFProtect()
login_manager_app = LoginManager(app)
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql,id)

@app.route('/')
@login_required
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts=data)


@app.route('/add_equipment', methods=['POST'])
@login_required
def add_equipment():
    if request.method == 'POST':
        numempleado = request.form['numempleado']
        usuario = request.form['usuario']
        accesorio = request.form['accesorio']
        descripcion = request.form['descripcion']
        fecha = request.form['fechaR']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (numempleado, usuario, accesorio, descripcion, fechaR) VALUES (%s, %s, %s, %s, %s)',
                    (numempleado, usuario, accesorio, descripcion, fecha))
        mysql.connection.commit()
        flash('Prestamo Realizado Exitosamente')
        return redirect(url_for('Index'))


@app.route('/edit/<id>')
@login_required
def get_equipment(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit-equipment.html', contact=data[0])


@app.route('/update/<id>', methods=['POST'])
@login_required
def update_equipmentt(id):
    if request.method == 'POST':
        fechaR = request.form['fechaR']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contacts SET fechaR = %s WHERE id = %s', (fechaR, id))
        mysql.connection.commit()
        flash('Fecha de Retorno Cambiado')
        return redirect(url_for('Index'))


@app.route('/reporte')
@login_required
def reporte():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('reporte.html', contacts=data)


@app.route('/delete/<string:id>')
@login_required
def delete_equipment(id):
    status = 1
    cur = mysql.connection.cursor()
    cur.execute('UPDATE contacts SET status = %s where id = %s', (status, id))
    mysql.connection.commit()
    flash('Prestamo Retornado Exitosamente')
    return redirect(url_for('Index'))


@app.route('/add-equipment')
@login_required
def addequipment():
    return render_template('add-equipment.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(mysql, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('Index'))
            else:
                flash("Contraseña Invalida.")
                return render_template('login.html')
        else:
            flash("Usuario no encontrado.")
            return render_template('login.html')
    else:
        return render_template('login.html')
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(401)
def not_found_endpoint(error):
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.run(port=3000)
