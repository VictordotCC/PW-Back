# 0. ejecutamos pip install flask flask-sqlalchemy flask-migrate flask-cors
# 1. Crear modelos
# 2. importamos las librerias de flask
# 8. comando para iniciar mi app flask: flask db init
# 9. comando para migrar mis modelos:   flask db migrate
# 10. comando para crear nuestros modelos como tablas : flask db upgrade
# 11. comando para iniciar la app flask: flask run
# 12. desde carpeta de front, ejecutar python -m http.server y acceder a localhost:8000
import os
from random import randint
from datetime import datetime
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Usuario, Comuna, Region, Producto, Venta, Detalle, Despacho
from flask_cors import CORS, cross_origin

# 3. instanciamos la app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.url_map.strict_slashes = False

app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

Migrate(app, db)

@app.route('/carrito', methods=['POST'])
def carrito():
    data = request.values
    cart = data.getlist('carrito[]')
    if len(cart) <= 0:
        return jsonify({None})
    cart_list = []
    for item in cart:
        cantidad = cart.count(item)
        producto = Producto.query.filter_by(codigo=item).first()
        producto_final = producto.serialize()
        producto_final["cantidad"] = cantidad
        if producto_final not in cart_list:
            cart_list.append(producto_final)              
    return jsonify(cart_list)

@app.route('/login', methods=['POST'])
def login():
    data = request.values
    user = data.get('email')
    password = data.get('pass')
    user = Usuario.query.filter_by(correo=user).first()
    if user is not None and user.password == password:
        return jsonify(user.serialize()), 200
    return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401

@app.route('/registrar', methods=['POST'])
def registro():
    data = request.values
    user = Usuario()

    user.primer_nombre = data.get('nombre')
    user.apellido_paterno = data.get('apellido')
    rut_con_dv = data.get('rut')
    #Trata el rut para quitar el dv
    rut = rut_con_dv.split('-')[0]
    user.rut = rut.replace('.', '')
    user.dv = rut_con_dv.split('-')[1]
    
    #sigue
    user.correo = data.get('email')
    user.direccion = data.get('direccion')
    region = data.get('Nombre_region')
    comuna = data.get('Nombre_comuna')   

    #tratamiento comuna
    comuna_id = Comuna.query.filter_by(nombre=comuna).first()
    if comuna_id is None:
        comuna_sql = Comuna()
        comuna_sql.nombre = comuna
        region_id = Region.query.filter_by(nombre=region).first()
        if region_id is None:
            region_sql = Region()
            region_sql.nombre = region
            region_sql.save()
            region_id = region_sql.id_region
        else:
            region_id = region_id.id_region
        comuna_sql.region_id = region_id
        comuna_sql.save()
        comuna_id = comuna_sql.id_comuna
    else:
        comuna_id = comuna_id.id_comuna
    user.comuna_id = comuna_id
    
    #sigue
    user.fono = data.get('fono')
    user.password = data.get('password')
    user.estado = True

    #Maneja sucripcion
    if data.get('suscripcion') == 'true':
        user.suscrito = True
    else:
        user.suscrito = False

    user.tipo = 'Cliente'

    if (Usuario.query.filter_by(rut=user.rut).first() is None
        and Usuario.query.filter_by(correo=user.correo).first() is None):
        user.save()
        return jsonify("Usuario registrado"), 200
    return jsonify("Usuario ya existe"), 400

@app.route('/registrar-producto', methods=['POST'])
def registrar_producto():
    file = request.files['v_file']
    file.save('static/img/' + file.filename) # guarda la imagen en la carpeta static/img
    data = request.values
    producto = Producto()
    producto.nombre = data.get('v_prod')
    producto.descripcion = data.get('v_desc')
    producto.categoria = data.get('v_cat')
    producto.valor_venta = data.get('v_precio')
    producto.stock = data.get('v_stock')
    producto.imagen = file.filename # guarda el nombre del archivo en la base de datos
    #genera el codigo de barras
    producto.codigo = producto.nombre[0:3] + producto.categoria[0:3] + str(randint(1000,9999))
    producto.estado = True

    if (Producto.query.filter_by(nombre=producto.nombre).first() is None):
        producto.save()
        return jsonify("Producto registrado"), 200
    return jsonify("Producto ya existe"), 400

@app.route('/productos', methods=['GET'])
def productos():
    productos = Producto.query.all()
    productos = list(map(lambda x: x.serialize(), productos))
    return jsonify(productos), 200

@app.route('/producto/<id>', methods=['GET', 'PUT', 'DELETE'])
def producto(id):
    if request.method == 'GET':
        producto = Producto.query.filter_by(id_producto=id).first()
        if producto is None:
            return jsonify({'error': 'Producto no encontrado'}), 404
        return jsonify(producto.serialize()), 200
    elif request.method == 'PUT':
        file = request.files['edit_file']
        producto = Producto.query.get(id)
        if producto is None:
            print("error al editar")
            return jsonify({'error': 'Producto no encontrado'}), 404
        if file.filename != '':
            os.remove('static/img/' + producto.imagen)
            file.save('static/img/' + file.filename)
            producto.imagen = file.filename
        data =request.values
        producto.nombre = data.get('edit_prod')
        producto.descripcion = data.get('edit_desc')
        producto.categoria = data.get('edit_cat')
        producto.valor_venta = data.get('edit_precio')
        producto.stock = data.get('edit_stock')
        producto.save()
        return jsonify({'estado':'Producto editado'}), 200
    elif request.method == 'DELETE':
        producto = Producto.query.get(id)
        if producto is None:
            return jsonify({'error': 'Producto no encontrado'}), 404
        os.remove('static/img/'+ producto.imagen)
        producto.delete()
        return jsonify(producto.serialize()), 200

@app.route('/comprar', methods=['POST'])
def comprar():
    data = request.values
    cart = data.getlist('carrito[]')
    userid = data.get('user_id')
    voucher = []
    subtotal = 0
    for item in cart:
        cantidad = cart.count(item)
        if cantidad > 0:
            producto = Producto.query.filter_by(codigo=item).first()
            subtotal += producto.valor_venta * cantidad
            #[Nombre, codigo, cantidad, valor unitario, valor total]
            voucher.append({'nombre': producto.nombre, 'codigo': producto.codigo, 'cantidad': cantidad, 'valor_unitario': producto.valor_venta, 'valor_total': producto.valor_venta * cantidad})
            producto.stock -= 1
            producto.save()
            cart = list(filter(lambda x: x != item, cart))

    #Calculo total venta e ingreso a bd
    iva = subtotal * 0.19
    total = subtotal + iva
    venta = Venta()
    venta.fecha = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    venta.sub_total = subtotal
    venta.iva = iva
    venta.total = total
    venta.estado = True
    venta.cliente_id = userid
    venta.save()

    #Ingreso a bd detalle venta
    for item in voucher:
         #[Nombre, codigo, cantidad, valor unitario, valor total]
        detalle = Detalle()
        detalle.cantidad = item['cantidad']
        detalle.valor = item['valor_total']
        detalle.estado = True
        detalle.venta_id = venta.id_venta
        detalle.producto_id = Producto.query.filter_by(codigo=item['codigo']).first().id_producto
        detalle.save()

    #Ingreso del Despacho
    despacho = Despacho()
    despacho.direccion = data.get('direccion')
    despacho.rut_recibe = data.get('user_rut')
    despacho.nombre_recibe = data.get('user_nombre')
    despacho.esto_despacho = 0 #0 = pendiente, 1 = preparando, 2 = en camino, 3 = entregado
    despacho.venta_id = venta.id_venta
    despacho.comuna_id = data.get('comuna')
    despacho.save()

    #actualizacion venta con id despacho
    venta = Venta.query.filter_by(id_venta=venta.id_venta).first()
    venta.despacho_id = despacho.id_despacho
    venta.save()

    voucherid = str(randint(1,9999)) + str(userid) + str(randint(1,9999))
    voucher.append({'voucher': voucherid, 'id_despacho': despacho.id_despacho, 'subtotal': subtotal, 'iva': iva, 'total': total})
    return jsonify(voucher), 200

    


#METODOS DEL PROFESOR


# Ruta para consultar todos los Usuarios
@app.route('/usuarios', methods=['GET'])
def getUsuarios():
    user = Usuario.query.all()
    user = list(map(lambda x: x.serialize(), user))
    return jsonify(user),200


# Borrar usuario
@app.route('/usuarios/<id>', methods=['DELETE'])
def deleteUsuario(id):
    user = Usuario.query.get(id)
    Usuario.delete(user)
    return jsonify(user.serialize()),200


# Modificar Usuario
@app.route('/usuarios/<id>', methods=['PUT'])
def updateUsuario(id):
    user = Usuario.query.get(id)

    user.primer_nombre = request.json.get('primer_nombre')
    user.segundo_nombre = request.json.get('segundo_nombre')
    user.apellido_paterno = request.json.get('apellido_paterno')
    user.apellido_materno = request.json.get('apellido_materno')
    user.direccion = request.json.get('direccion')

    Usuario.save(user)

    return jsonify(user.serialize()),200


# 4. Configurar los puertos nuestra app 
if __name__ == '__main__':
    app.run(port=5000, debug=True)