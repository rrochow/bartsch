# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite3
from flask import (
    Flask,
    render_template,
    url_for,
    request,
    flash,
    redirect,
    session
)

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form["user"]
        password = request.form["password"]
        db = connect_db2()
        result = db.execute('SELECT correo, clave FROM cliente WHERE correo=? AND clave = ?',[user, password])
        matches = result.fetchall()
        db.close()
        if len(matches) > 0: #The user and pass combination exits
            user_data = matches[0]
            session['username'] = user
            return redirect(url_for('show_home'))
        else:
            return render_template('form.html')      
    else:
        return render_template('carro.html')

@app.route('/logout')
def logout():
    # remove the user from the session if it's there
    session.pop('username',None)
    return redirect(url_for('show_home'))

def connect_db():
    """Retorna una conexión a la BD"""
    path_to_db = 'entry.db'
    rv = sqlite3.connect(path_to_db)
    rv.row_factory = sqlite3.Row
    return rv

def connect_db2():
    """Retorna una conexión a la BD"""
    path_to_db = 'basedatos.db'
    rv = sqlite3.connect(path_to_db)
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Crea las tablas y datos de prueba"""
    db = connect_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


@app.route('/')
def show_home():
    return render_template('home.html')

@app.route('/bartsch')
def show_bartsch():
    return render_template('quienes_somos.html')

@app.route('/cervezas')
def show_cervezas():
    db = connect_db2()
    cur = db.execute('SELECT nombre, descripcion, grados,img_url FROM cerveza ORDER BY id DESC')
    cerveza = cur.fetchall()
    db.close()
    return render_template('productos.html', cervezas=cerveza)

@app.route('/carro')
def new_compra():
    db = connect_db2()
    cur = db.execute('SELECT p.id,p.nombre, p.descripcion,p.precio_neto,b.stock,p.img_url FROM producto p,bodega b WHERE  p.id=b.id_producto ORDER BY p.id DESC')
    producto = cur.fetchall()
    db.close()

    db = connect_db2()
    cur = db.execute('SELECT nombre, descripcion,grados,img_url FROM cerveza ORDER BY id DESC')
    cerveza = cur.fetchall()
    db.close()

    return render_template('carro.html', productos=producto, cervezas=cerveza)

@app.route('/carro', methods=['GET', 'POST'])
def show_carro():
    if request.method == 'GET':
        return "Ajilao"
    elif request.method == 'POST':
    	if request.form['boton_carro'] == '5':
    		return render_template('index.php')
    	else:
    		return request.form['cantidad']
    else:
        return "Acceso denegado"

@app.route('/perfil')
def show_perfil():
    return render_template('perfil.html')

@app.route('/empresa')
def show_empresa():
    return render_template('perfil_empresa.html')

@app.route('/cuenta')
def show_cuenta():
    return render_template('perfil_cuenta.html')


@app.route('/form', methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        db = connect_db()
        db.execute(
            'INSERT INTO entry (title, description) values (?, ?)',[title, description]
        )
        db.commit()
        db.close()
        return u"Operación exitosa"
    else:
        return "Acceso denegado"

@app.route('/registro', methods=['GET', 'POST'])
def new_registro():
    if request.method == 'GET':
        return render_template('registrarse.html')
    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        db = connect_db()
        db.execute(
            'INSERT INTO entry (title, description) values (?, ?)',[title, description])
        db.commit()
        db.close()
        return u"Operación exitosa"
    else:
        return "Acceso denegado"

@app.route('/contacto', methods=['GET', 'POST'])
def new_contacto():
    if request.method == 'GET':
        return render_template('contacto.html')
    elif request.method == 'POST':
    	nombre = request.form['nombre']
    	email = request.form['email']
    	mensaje = request.form['mensaje']
    	return mensaje
    else:
        return "Acceso denegado"

if __name__ == "__main__":
    app.run(debug=True)















