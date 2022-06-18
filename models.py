from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Region(db.Model):
    __tablename__ = 'Region'
    id_region = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Comuna(db.Model):
    __tablename__ = 'Comuna'
    id_comuna = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('Region.id_region'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'region_id': self.region_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    rut = db.Column(db.Integer, nullable=False)
    dv = db.Column(db.Integer, nullable=True)
    primer_nombre = db.Column(db.String(250), nullable= False)
    segundo_nombre = db.Column(db.String(250), nullable= True)
    apellido_paterno = db.Column(db.String(250), nullable= False)
    apellido_materno = db.Column(db.String(250), nullable= True)
    direccion = db.Column(db.String(250), nullable= False)
    fono = db.Column(db.Integer, nullable=False)
    correo = db.Column(db.String(250), nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    comuna_id = db.Column(db.Integer, db.ForeignKey('Comuna.id_comuna'), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    suscrito = db.Column(db.Boolean, nullable=False)

    def serialize(self):
        return{
            "id_usuario": self.id_usuario,
            "rut": self.rut,
            "dv": self.dv,
            "primer_nombre": self.primer_nombre,
            "segundo_nombre": self.segundo_nombre,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "direccion": self.direccion,
            "fono": self.fono,
            "correo": self.correo,
            "estado": self.estado,
            "comuna_id": self.comuna_id            
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Producto(db.Model):
    __tablename__ = 'Producto'
    id_producto = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(250), nullable=False)
    nombre = db.Column(db.String(250), nullable=False)
    categoria = db.Column(db.String(250), nullable=False)
    valor_venta = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String(250), nullable=False)
    imagen= db.Column(db.String(250), nullable=False)
    estado = db.Column(db.Boolean, nullable=False)

    def serialize(self):
        return{
            "id_producto": self.id_producto,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "valor_venta": self.valor_venta,
            "stock": self.stock,
            "descripcion": self.descripcion,
            "imagen": self.imagen,
            "estado": str(self.estado)
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Descuento(db.Model):
    __tablename__ = 'Descuento'
    id_descuento = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    porcentaje = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Boolean, nullable=False)

    def serialize(self):
        return{
            "id_descuento": self.id_descuento,
            "nombre": self.nombre,
            "fecha": self.fecha,
            "porcentaje": self.porcentaje,
            "estado": self.estado
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Descuento_Producto(db.Model):
    __tablename__ = 'Descuento_Producto'
    producto_id = db.Column(db.Integer, db.ForeignKey('Producto.id_producto'), primary_key=True)
    descuento_id = db.Column(db.Integer, db.ForeignKey('Descuento.id_descuento'), primary_key=True)
    fecha_inicio = db.Column(db.String(20), nullable=True)
    fecha_termino = db.Column(db.String(20), nullable=True)

    def serialize(self):
        return{
            "producto_id": self.producto_id,
            "descuento_id": self.descuento_id,
            "fecha_inicio": self.fecha_inicio,
            "fecha_termino": self.fecha_termino
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Suscripcion(db.Model):
    __tablename__ = 'Suscripcion'
    id_suscripcion = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.String(20), nullable=False)
    fecha_termino = db.Column(db.String(20), nullable=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Usuario.id_usuario'), nullable=False)

    def serialize(self):
        return{
            "id_suscripcion": self.id_suscripcion,
            "fecha_inicio": self.fecha_inicio,
            "fecha_termino": self.fecha_termino,
            "cliente_id": self.cliente_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Donacion(db.Model):
    __tablename__ = 'Donacion'
    id_donacion = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Usuario.id_usuario'), nullable=False)

    def serialize(self):
        return{
            "id_donacion": self.id_donacion,
            "valor": self.valor,
            "fecha": self.fecha,
            "cliente_id": self.cliente_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Despacho(db.Model):
    __tablename__ = 'Despacho'
    id_despacho = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(250), nullable=False)
    fecha_entrega = db.Column(db.String(20), nullable=True)
    rut_recibe = db.Column(db.String(250), nullable=True)
    nombre_recibe = db.Column(db.String(250), nullable=True)
    esto_despacho = db.Column(db.Integer, nullable=False)
    venta_id = db.Column(db.Integer, db.ForeignKey('Venta.id_venta'), nullable=False)
    comuna_id = db.Column(db.Integer, db.ForeignKey('Comuna.id_comuna'), nullable=False)

class Venta(db.Model):
    __tablename__ = 'Venta'
    id_venta = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    descuento = db.Column(db.Integer, nullable=True)
    sub_total = db.Column(db.Integer, nullable=False)
    iva = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Usuario.id_usuario'), nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('Usuario.id_usuario'), nullable=False)
    despacho_id = db.Column(db.Integer, db.ForeignKey('Despacho.id_despacho'), nullable=True)

    def serialize(self):
        return{
            "id_venta": self.id_venta,
            "fecha": self.fecha,
            "descuento": self.descuento,
            "sub_total": self.sub_total,
            "iva": self.iva,
            "total": self.total,
            "estado": self.estado,
            "cliente_id": self.cliente_id,
            "vendedor_id": self.vendedor_id,
            "despacho_id": self.despacho_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Detalle(db.Model):
    __tablename__ = 'Detalle'
    id_detalle = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Integer, nullable=False)
    descuento = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    venta_id = db.Column(db.Integer, db.ForeignKey('Venta.id_venta'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('Producto.id_producto'), nullable=False)

    def serialize(self):
        return{
            "id_detalle": self.id_detalle,
            "cantidad": self.cantidad,
            "valor": self.valor,
            "descuento": self.descuento,
            "estado": self.estado,
            "venta_id": self.venta_id,
            "producto_id": self.producto_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


