# -*- coding: utf-8 -*-
#libreria validacion de mail solamente chrome
import re
#libreria de servidor de correo
from flask.ext.mail import Message, Mail
from sqlite3 import dbapi2 as sqlite3
from flask import (
    Flask,
    render_template,
    url_for,
    request,
    flash,
    redirect,
    session,
)
#inicializacion del email
DEBUG = True
SECRET_KEY = 'hidden'
USERNAME = 'secret'
PASSWORD = 'secret'
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=465
MAIL_USE_TLS = False
MAIL_USE_SSL= True
MAIL_USERNAME = 'testcerveza@gmail.com'
MAIL_PASSWORD = 'grupotaller'

#variable carro tendra la cantidad total y producto,cantidad
carro = []
total_carro = 0
total_compra = 0

app = Flask(__name__)

app.config.from_object(__name__)
mail = Mail(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#conexion a la base de datos
def connect_db():
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

#Login y Logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form["user"]
        password = request.form["password"]
        db = connect_db()
        result = db.execute('SELECT correo, clave FROM cliente WHERE correo=? AND clave = ?',[user, password])
        matches = result.fetchall()
        db.close()
        if len(matches) > 0: #The user and pass combination exits
            user_data = matches[0]
            session['username'] = user
            return redirect(url_for('show_home'))
        else:
            return render_template('home.html')      
    else:
        return render_template('carro.html')

@app.route('/logout')
def logout():
    # remove the user from the session if it's there
    session.pop('username',None)
    #reiniciamos variables del carro de compras
    global carro
    global total_carro
    total_carro = 0
    del carro
    carro = []   
    return redirect(url_for('show_home'))


@app.route('/')
def show_home():
    return render_template('home.html')

@app.route('/bartsch')
def show_bartsch():
    return render_template('quienes_somos.html')

@app.route('/cervezas')
def show_cervezas():
    db = connect_db()
    cur = db.execute('SELECT nombre, descripcion, grados,img_url FROM cerveza ORDER BY id DESC')
    cerveza = cur.fetchall()
    db.close()
    return render_template('cervezas.html', cervezas=cerveza)

#carro de compras

@app.route('/carro')
def show_productos():
    db = connect_db()
    cur = db.execute('SELECT id,nombre, descripcion,precio_neto,img_url FROM producto ORDER BY id DESC')
    producto = cur.fetchall()
    db.close()

    return render_template('carro_productos.html', productos=producto,cantidad = total_carro)

@app.route('/carro/<int:id_producto>/<int:cantidad>')
def agregar_al_carro(id_producto,cantidad):
    global carro
    global total_carro
    total_carro = cantidad + total_carro
    
    #obtenemos datos del producto
    db = connect_db()
    cur = db.execute(
        'SELECT p.nombre, p.descripcion,b.stock,p.precio_neto,p.img_url FROM producto p,bodega b WHERE  p.id=b.id_producto and p.id = ?',[id_producto]
    )
    consulta = cur.fetchall()
    db.close()

    for salida in consulta:
        nombre=salida['nombre']
        descripcion=salida['descripcion']
        stock=salida['stock']
        precio_neto=salida['precio_neto']
        img_url=salida['img_url']

    #agregamos al carro la lista producto={id,cantidad}
    producto = [id_producto,cantidad,nombre,descripcion,stock,precio_neto,img_url]
    hit = 'false'
    if len(carro)>0:
        for i in range(len(carro)):
            if id_producto == carro[i][0]:
                carro[i][1]= carro[i][1]+cantidad
                hit = 'true'
                return redirect(url_for('show_productos'))
        if hit == 'false':
            carro.append(producto)
            return redirect(url_for('show_productos'))    
    else:
        carro.append(producto)
        return redirect(url_for('show_productos'))



@app.route('/carro_compras')
def show_carro():
    global total_compra
    total_compra = 0
    if total_carro>0:
        for i in range(len(carro)):
            total_compra = carro[i][1] * carro[i][5] + total_compra
        return render_template('carro.html',carro=carro,total=total_compra)
    else:
        return render_template('carro.html')

@app.route('/carro_compras/<int:id_producto>/<int:cantidad>')
def eliminar_del_carro(id_producto,cantidad):    
    global carro
    global total_carro
    total_carro = total_carro - cantidad

    for i in range(len(carro)):
        if id_producto == carro[i][0]:
            del carro[i]
            return redirect(url_for('show_carro'))



#Perfil del Cliente

@app.route('/perfil')
def show_perfil():
    return render_template('perfil.html')

@app.route('/empresa')
def show_empresa():
    return render_template('perfil_empresa.html')

@app.route('/cuenta')
def show_cuenta():
    return render_template('perfil_cuenta.html')

#registro de usuario

def is_email_address_valid(correo):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", correo):
        return False
    else:
        return True

@app.route('/registro', methods=['GET','POST'])
def new_registro():
    if request.method == 'GET':
        return render_template("registrarse.html")
    elif request.method == 'POST':
        correo = request.form['correo']
        db = connect_db()
        result = db.execute('SELECT correo FROM cliente WHERE correo=?', [correo])
        matches = result.fetchall()
        db.close()

        if len(matches) > 0: #The user and pass combination exits
            return render_template('registrarse.html',error='correo ya registrado')
        else:
            correo = request.form['correo']
            clave = request.form['clave']
            db = connect_db()
            db.execute(
                'INSERT INTO cliente (correo, clave) values (?, ?)',[correo, clave]
            )
            db.commit()
            db.close()            
            return render_template('registrarse.html',error='Registrado con exito')  
    else:
        return render_template("home.html")


#Metodos Email

@app.route('/contacto', methods=['GET', 'POST'])
def new_contacto():
    if request.method == 'GET':
        return render_template('contacto.html')
    elif request.method == 'POST':
        mensaje = Message(
            'Contacto-Cerveza Bartsch',
            sender=request.form['nombre'],
            recipients=['testcerveza@gmail.com']
        )
        mensaje.body = "De : "+request.form['nombre']+"\n\n"+request.form['mensaje'] + "\n\nCorreo : " +request.form['email']
        mail.send(mensaje)
        return "Send"


if __name__ == "__main__":
    app.run(debug=True)















