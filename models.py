from index import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime as dt
from datetime import timedelta



class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80))
    usuario = db.Column(db.String(80))
    token = db.Column(db.String(80))
    refreshtoken = db.Column(db.String(80))
    tipo = db.Column(db.Integer)
    alta = db.Column(db.DateTime)
    baja = db.Column(db.DateTime)
    palabrasminimas = db.Column(db.Integer)
    palabrasminimassi = db.Column(db.Boolean)
    tiempodeespera = db.Column(db.Integer)
    tiempodeesperasi = db.Column(db.Boolean)
    lunesnorespuesta = db.Column(db.Boolean)
    martesnorespuesta = db.Column(db.Boolean)
    miercolesnorespuesta = db.Column(db.Boolean)
    juevesnorespuesta = db.Column(db.Boolean)
    viernesnorespuesta = db.Column(db.Boolean)
    sabadonorespuesta = db.Column(db.Boolean)
    domingonorespuesta = db.Column(db.Boolean)
    horainiciobloqueo = db.Column(db.Integer)
    minutoiniciobloqueo = db.Column(db.Integer)
    horafinbloqueo = db.Column(db.Integer)
    minutofinbloqueo = db.Column(db.Integer)
    bloqueotiemposi = db.Column(db.Boolean)
    bloqueadospreguntas = db.Column(db.String(200))
    bloqueadoscompras = db.Column(db.String(200))
    mensajes = db.Column(db.Integer)
    respuestas = db.Column(db.Integer)
    diarespuesta = db.Column(db.Text)
    horarespuesta = db.Column(db.Text)
    diamensaje = db.Column(db.Text)
    horamensaje = db.Column(db.Text)
    respuestasauto = db.Column(db.Integer)
    mensajesauto = db.Column(db.Integer)

    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    def __repr__(self):
        return f'<Usuarios {self.usuario}>'
    @staticmethod
    def get_by_id(id):
        return Usuarios.query.get(id)
    @staticmethod
    def get_by_usuario(usuario):
        return Usuarios.query.filter_by(usuario=usuario)
    @staticmethod
    def get_by_tipo(tipo):
        return Usuarios.query.filter_by(tipo=tipo)
    @staticmethod
    def get_by_baja(baja):
        return Usuarios.query.filter_by(baja=baja)
    @staticmethod
    def get_by_alta(alta):
        return Usuarios.query.filter_by(alta=alta)
    @staticmethod
    def get_all():
        return Usuarios.query.all()


class Mensajes(db.Model):
    __tablename__ = 'mensajes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    uso = db.Column(db.Integer)
    texto = db.Column(db.Text)
    tiempo = db.Column(db.Integer)
    full = db.Column(db.Boolean)
    flex = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    dia = db.Column(db.Integer)
    hora = db.Column(db.Integer)
    minutos = db.Column(db.Integer)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(id):
        return Mensajes.query.get(id)
    @staticmethod
    def get_by_user_id(user_id):
        return Mensajes.query.get(user_id)
    

#1 Aviso de compra. 2 Envío Realizado. 3 Mensaje de Agradecimiento. 4 venta de fin de semana. 5 Guía de envío impresa.
#6 Envío a tratar con el comprador. 7 Mercado Envíos. 8 Mensaje Programado. 9 digital. 
# día 1 sabado, día 2 domingo, día 3 ambos.

class Primermensaje(db.Model):
    __tablename__ = 'primermensaje'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    uso = db.Column(db.Integer)
    texto = db.Column(db.Text)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
#1 global, 2 full, 3 flex 4 normal, 5 a tratar


class Especiales(db.Model):
    __tablename__ = 'especiales'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    uso = db.Column(db.Integer)
    texto = db.Column(db.Text)
    status = db.Column(db.Boolean)
    exclusivo = db.Column(db.Boolean)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Mensajesflex(db.Model):
    __tablename__ = 'mensajesflex'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    uso = db.Column(db.Integer)
    texto = db.Column(db.Text)
    status = db.Column(db.Boolean)
    exclusivo = db.Column(db.Boolean)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
#1 creada,  2 enviada, 3 entregada, 4 general

class Full(db.Model):
    __tablename__ = 'full'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    texto = db.Column(db.Text)
    status = db.Column(db.Boolean)
    exclusivo = db.Column(db.Boolean)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

#1 al crear orden. #2 al entregar orden
class Iniciales(db.Model):
    __tablename__ = "inicial"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    uso = db.Column(db.Integer)
    texto = db.Column(db.Text)
    status = db.Column(db.Boolean)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

#1 Fullfilment. #2 MercadoEnvíos. #3 Flex

class Promesa(db.Model):
    __tablename__ = "promesa"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    inicio = db.Column(db.Integer)
    final = db.Column(db.Integer)
    tipo = db.Column(db.Integer)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

#1 Venta Creada. #2 Venta Enviada

class Publicaciones(db.Model):
    __tablename__ = 'publicaciones'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    pub_id = db.Column(db.String(80))
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Encrespuestas(db.Model):
    __tablename__ = 'encrespuestas'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    encabezado = db.Column(db.Text)
    incluirencabezado = db.Column(db.Boolean)
    pie = db.Column(db.Text)
    incluirpie = db.Column(db.Boolean)
    palabrasmaximas = db.Column(db.Integer)
    palabrasmaximassi = db.Column(db.Boolean)
    palabrasprohibidas = db.Column(db.Text)
    reputacion = db.Column(db.Integer)
    borrarpregunta = db.Column(db.Boolean)
    bloquearusuario = db.Column(db.Boolean)
    palabrasprohibidassi = db.Column(db.Boolean)
    diasprohibidos = db.Column(db.String(80))
    horainiciobloqueo = db.Column(db.Integer)
    minutoiniciobloqueo = db.Column(db.Integer)
    horafinbloqueo = db.Column(db.Integer)
    minutofinbloqueo = db.Column(db.Integer)
    bloqueotiemposi = db.Column(db.Boolean)
    unirrespuestas = db.Column(db.Boolean)
    respuestasunidas = db.Column(db.Integer)
    unirrespuestaglobal = db.Column(db.Boolean)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_user(user_id):
        return Encrespuestas.query.filter_by(user_id=user_id)
    

class Codigos(db.Model):
    __tablename__ = 'codigos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    pub_id = db.Column(db.Integer, db.ForeignKey('publicaciones.id', ondelete='CASCADE'), nullable=False)
    codigos = db.Column(db.String(200))
    status = db.Column(db.Boolean)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()


class Respuestas(db.Model):
    __tablename__ = 'respuestas'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    palabrasclave = db.Column(db.String(80))
    texto = db.Column(db.Text)
    numero =  db.Column(db.Integer)
    pub_id = db.Column(db.String(200))
    uso = db.Column(db.Integer)
    activo = db.Column(db.Boolean)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_pub_id(pub_id):
        return Respuestas.query.filter(pub_id==pub_id)
    @staticmethod
    def get_by_unica_user(user_id):
        return Respuestas.query.filter(user_id==user_id, Respuestas.uso == 1)
    @staticmethod
    def get_by_global_user(user_id):
        return Respuestas.query.filter(user_id==user_id, Respuestas.uso == 2)
    @staticmethod
    def get_by_pub_user(user_id):
        return Respuestas.query.filter(user_id==user_id, Respuestas.uso == 3)
    @staticmethod
    def get_by_palabra_user(user_id, texto):
        return Respuestas.query.filter(user_id==user_id, Respuestas.palabrasclave.ilike(texto), Respuestas.uso==3)

#uso 1 = unica 2 = global 3= por publicaciones 4=por publicaciones exclusiva


class Preguntas(db.Model):
    __tablename__ = 'preguntas'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    pub_id = db.Column(db.Integer, db.ForeignKey('publicaciones.id', ondelete='CASCADE'), nullable=False)
    texto = db.Column(db.Text)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

#uso 1 = unica 2 = global 3= por publicaciones

class Sinrespuesta(db.Model):
    __tablename__ = 'sinrespuesta'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    pub_id = db.Column(db.String(40))
    texto = db.Column(db.Text)
    numero = db.Column(db.String(15))
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @staticmethod
    def get_by_user(user_id):
        return Sinrespuesta.query.filter_by(user_id=user_id)
    @staticmethod
    def get_by_numero(numero):
        return Sinrespuesta.query.filter_by(numero=numero)

class Ventas(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    pub_id = db.Column(db.String(80))
    user_id = db.Column(db.Integer)
    dia = db.Column(db.DateTime)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_usuario_hoy(user_id):
        return Usuarios.query.filter(
            Ventas.user_id == user_id,
            Ventas.dia > dt.today() - timedelta(days=1))
    @staticmethod
    def get_by_usuario_semana(user_id):
        return Usuarios.query.filter(
            Ventas.user_id == user_id,
            Ventas.dia > dt.today() - timedelta(days=7))
    @staticmethod
    def get_by_usuario_mes(user_id):
        return Usuarios.query.filter(
            Ventas.user_id == user_id,
            Ventas.dia > dt.today() - timedelta(days=30))
    @staticmethod
    def get_by_usuario(user_id):
        return Usuarios.query.filter(Ventas.user_id == user_id)