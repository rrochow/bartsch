# -*- coding: utf-8 -*-
#libreria validacion de mail solamente chrome
#libreria time para trabajar con fechas
import re,time
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

#inicializamos variables
def init_variables():
    global carro
    global total_carro
    total_carro = 0
    total_compra = 0
    del carro
    carro = []
    pass 

##################
#Login y Logout  #
##################

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form["user"]
        password = request.form["password"]
        db = connect_db()
        result = db.execute('SELECT id, correo, clave FROM cliente WHERE correo=? AND clave = ?',[user, password])
        matches = result.fetchall()
        db.close()

        for cliente in matches:
            id_user = cliente['id']

        if len(matches) > 0: #The user and pass combination exits
            user_data = matches[0]
            session['username'] = user
            session['id'] = id_user
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
    init_variables()

    return redirect(url_for('show_home'))

#######################
# Despliegue de Datos #
#######################

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

###################
#carro de compras #
###################

@app.route('/carro')
def show_productos():
    db = connect_db()
    cur = db.execute('SELECT id,nombre, descripcion,precio_neto,img_url FROM producto ORDER BY id_cerveza ASC')
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

@app.route('/reserva')
def crear_reserva():
    #insertamos una nueva reserva
    fecha = time.strftime("%d/%m/%Y")
    db = connect_db()
    db.execute(
        'INSERT INTO reserva (fecha,tipo_documento,id_cliente) VALUES (?, ?, ?)',
        [fecha, 'boleta',session['id']]
    )
    db.commit()
    db.close()

    #obtenemos el id de la reserva nueva
    db = connect_db()
    cur = db.execute(
        'SELECT MAX(id) AS id FROM reserva WHERE id_cliente=?',[session['id']]
    )
    query = cur.fetchall()
    db.close()

    for reserva in query:
        id_reserva = reserva['id']

    #insertamos los productos asociados
    db = connect_db()    
    for i in range(len(carro)):
        cur = db.execute(
            'INSERT INTO producto_reserva (id_reserva,id_producto,cantidad) VALUES (?,?,?)',
            [ id_reserva, carro[i][0], carro[i][1] ]
        )
        db.commit()    
    db.close()
    #reiniciamos el carro
    init_variables()
    return render_template("carro_reserva.html")

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


#####################
#Perfil del Cliente #
#####################

#Mostrar y Modificar Datos del Cliente
def datos_cliente():
    db = connect_db()
    cur = db.execute(
        'SELECT rut,nombre,apellido,direccion,telefono FROM cliente WHERE correo=?',
        [session['username']]
    )
    cliente = cur.fetchall()
    db.close()
    return cliente      

@app.route('/perfil')
def show_perfil():
    cliente = datos_cliente()  
    return render_template('perfil.html',cliente=cliente)

@app.route('/perfil', methods=['GET','POST'])
def modificar_perfil():
    if request.method == 'POST':
        rut = request.form['rut']
        nom = request.form['nombre']
        ape = request.form['apellido']
        dire = request.form['direccion']
        tele = request.form['telefono']
        db = connect_db()
        db.execute(
            'UPDATE cliente SET rut=?,nombre=?,apellido=?,direccion=?,telefono=? WHERE correo=?',
            [rut,nom,ape,dire,tele,session['username']]
        )
        db.commit()
        db.close()
        cliente = datos_cliente()
        mensaje = "(datos modificados)"
        return render_template('perfil.html',cliente=cliente,mensaje=mensaje)          
    else:
        return u""

#Mostrar y modificar datos de la empresa
def datos_empresa():
    db = connect_db()
    cur = db.execute(
        'SELECT rut,nombre,direccion,ciudad,telefono,email FROM empresa_cliente WHERE id_cliente=?',
        [session['id']]
    )
    empresa = cur.fetchall()
    db.close()
    return empresa  

@app.route('/empresa')
def show_empresa():
    empresa = datos_empresa()
    return render_template('perfil_empresa.html',empresas=empresa)

@app.route('/empresa_modificar', methods=['GET','POST'])
def modificar_empresa():
    if request.method == 'POST':
        rut = request.form['rut']
        nom = request.form['nombre']
        dire = request.form['direccion']
        ciu = request.form['ciudad']
        tel = request.form['telefono']
        cor = request.form['correo']
        db = connect_db()
        db.execute(
            'UPDATE empresa_cliente SET rut=?,nombre=?,direccion=?,ciudad=?,telefono=?,email=? WHERE id_cliente=?',
            [rut,nom,dire,ciu,tel,cor,session['id']]
        )
        db.commit()
        db.close()
        empresa = datos_empresa()
        return render_template('perfil_empresa.html',empresas=empresa,mensaje='datos modificados con exito')          
    else:
        return u""

#Mostrar y modificar datos de la cuenta cliente
@app.route('/cuenta')
def show_cuenta():
    return render_template('perfil_cuenta.html')

@app.route('/cuenta', methods=['GET','POST'])
def modificar_cuenta():
    if request.method == 'POST':
        #validamos claves
        if request.form['clave1']=='' or request.form['clave2']=='':
            return render_template('perfil_cuenta.html',mensaje='campo vacio de claves')

        if request.form['clave1'] != request.form['clave2']:
            return render_template('perfil_cuenta.html',mensaje='no coinciden las claves')

        db = connect_db()
        db.execute(
            'UPDATE cliente SET clave=? WHERE correo=?',
            [request.form['clave1'],session['username']]
        )
        db.commit()
        db.close()

        return render_template('perfil_cuenta.html',mensaje='clave modificada con exito')          
    else:
        return u""

######################
#registro de usuario #
######################

@app.route('/registro', methods=['GET','POST'])
def new_registro():
    if request.method == 'GET':
        return render_template("registrarse.html")
    elif request.method == 'POST':

        #validamos los datos correctos
        if request.form['correo']=='':
            return render_template('registrarse.html',error='campo de correo vacio')

        if request.form['clave1']=='' or request.form['clave2']=='':
            return render_template('registrarse.html',error='campo vacio de claves')

        if request.form['clave1'] != request.form['clave2']:
            return render_template('registrarse.html',error='no coinciden las claves')

        #verificamos que la cuenta no exista
        correo = request.form['correo']
        db = connect_db()
        result = db.execute('SELECT correo FROM cliente WHERE correo=?', [correo])
        matches = result.fetchall()
        db.close()

        if len(matches) > 0:
            return render_template('registrarse.html',error='error: La cuenta ya existe')
        else:
            #si la cuenta no existe  agregamos la nueva cuenta
            correo = request.form['correo']
            clave = request.form['clave1']
            db = connect_db()
            db.execute(
                'INSERT INTO cliente (correo, clave) values (?, ?)',[correo, clave]
            )
            db.commit()
            db.close()            
            return render_template('registrarse.html',error='Cuenta creada con exito')  
    else:
        return render_template("home.html")


#Metodos Email
def is_email_address_valid(correo):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", correo):
        return False
    else:
        return True

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















