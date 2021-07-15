from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from requests_oauthlib import OAuth2Session
from flask.json import jsonify
from fusionauth.fusionauth_client import FusionAuthClient
import json
import os
import requests
import urllib
from datetime import datetime as dt
from datetime import timedelta
from dotenv import dotenv_values
config = dotenv_values(".env")


app = Flask(__name__)
app.secret_key = config["app_secret_key"]

## app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:sososo@localhost:5432/usuarios'
app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
redirect_uri = "https://mercadobot3.herokuapp.com/inicio"
client_secret = config["client_secret"]
client_id = config["client_id"]




@app.route("/")
def home():
    if 'username' in session:
        return redirect(url_for('perfil'))
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/reset")
def reset():
    from models import Usuarios
    from models import Mensajes
    from models import Primermensaje
    from models import Especiales
    from models import Mensajesflex
    from models import Full
    from models import Iniciales
    from models import Promesa
    from models import Publicaciones
    from models import Encrespuestas
    from models import Codigos
    from models import Respuestas
    from models import Preguntas
    from models import Ventas
    from models import Sinrespuesta
    db.create_all()
    db.session.commit()

@app.route("/perfil")
def perfil():
    from models import Usuarios
    from models import Ventas
    if 'username' in session:
        username = session['username']
    else:
        username = ""
    user = Usuarios.get_by_id(int(username))
    bearer = "Bearer " + user.token
    headers= {'Authorization': bearer}
    uri = "https://api.mercadolibre.com/users/" + user.usuario + "/items/search/"
    response = requests.get(uri, headers=headers)
    username = response.text + "xxx" + uri + "xxx" + bearer
    inicio = 0
    print(response.text)
    print(response.json()['results'])
    final = str(response.json()['results']).find(',',inicio)
    print(uri)
    print(response.text)
    print(bearer)
    print(username)
    n = 0 
    lista = []
    print(response.text)

    while n < 100:
        print("b")
        print(inicio)
        print(final)
        print(response.json()['results'][inicio:final-1])
        if final == -1:
            break
        if n == 0:
            lista.append(response.json()['results'][inicio:final])
        else:
            lista.append(response.json()['results'][inicio:final-1])
        inicio = final+2
        if inicio > len(response.json()['results']):
            break
        final = response.json()['results'].find(',',inicio+2) 
        n = n+1
    uri = "https://api.mercadolibre.com/items?ids="
    print("nueva uri es")
    print(uri)
    n = 0
    print("c")
    print(lista)
    lista = response.json()['results']
    while n < len(lista):
        print("d")
        if n == 0:
            uri = uri + lista[n]
            print(lista[n])
        else:
            uri = uri + "," + lista[n]
        n = n + 1
    print("e")
    print(uri)
    response = requests.get(uri, headers=headers)
    print("laqueva")
    print(response.text)
    listaProductos = []
    listaPrecios = []
    listaPermalink = []
    listaVendidos = []
    listaPictures = []
    listaStock =[]
    lista
    n=0
    inicio = response.text.find('"title":')+9
    final = response.text.find('"',inicio+2)
    print(uri)
    while n < 10:
        print("f")
        if response.text[inicio:final-1] in listaProductos or uri == 'https://api.mercadolibre.com/items?ids=':
            break
        listaProductos.append(response.text[inicio:final-1])
        listaPrecios.append(response.text[response.text.find('"price"',final)+8:response.text.find(',',response.text.find('"price"',final))])
        listaVendidos.append(response.text[response.text.find('"sold_quantity"',final)+16:response.text.find(',',response.text.find('"sold_quantity"',final))])
        listaStock.append(response.text[response.text.find('"available_quantity"',final)+21:response.text.find(',',response.text.find('"available_quantity"',final))])
        listaPermalink.append(response.text[response.text.find('"permalink"',final)+13:response.text.find(',',response.text.find('"permalink"',final))-1])
        iniciopictures = response.text.find('"pictures"',final)
        iniciourl = response.text.find('"url":',iniciopictures,iniciopictures+100)
        if iniciourl == -1:
            listaPictures.append("")
        else:
            listaPictures.append(response.text[iniciourl+7:response.text.find(",",iniciourl)-1])
        inicio = response.text.find('"title":',final)+9
        final = response.text.find('"',inicio+2)
        if inicio < 10:
            break
        n = n+1
    if Ventas.get_by_usuario(user.id) is None:
        ventashoy = 0
        ventassemanal = 0
        ventasmensual = 0
    else:
        ventashoy = Ventas.get_by_usuario_hoy(user.id).count()
        ventassemanal = Ventas.get_by_usuario_semana(user.id).count()
        ventasmensual = Ventas.get_by_usuario_mes(user.id).count()
    return render_template('perfil.html',ventashoy=ventashoy,ventassemanal=ventassemanal,ventasmensual=ventasmensual,productos=listaProductos,precios=listaPrecios,vendidos=listaVendidos,stock=listaStock,permalink=listaPermalink,pictures=listaPictures, user=user)

@app.route("/cerrarsesion")
def cerrarsesion():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

@app.route("/inicio")
def inicio():
    from models import Usuarios
    codigo = request.url
    codigo = codigo[codigo.find("=")+1:]
    headers = {'accept': 'application/json','content-type': 'application/x-www-form-urlencoded'}
    params = {'grant_type' : 'authorization_code', 'client_id' : client_id,'client_secret' : client_secret,'code' : codigo,'redirect_uri' : redirect_uri}
    uri = "https://api.mercadolibre.com/oauth/token"
    response = requests.post(uri, params=urllib.parse.urlencode(params), data=params, headers=headers)
    usuario = response.text[response.text.find('"user_id":')+10:response.text.find(',',response.text.find('"user_id":'))]
    token = response.text[response.text.find('"access_token":')+16:response.text.find(',',response.text.find('"access_token":'))-1]
    refreshtoken = response.text[response.text.find('"refresh_token":')+17:response.text.find(',',response.text.find('"refresh_token":'))-1]
    user = Usuarios.get_by_usuario(usuario).first()
    if user is None:
        bearer = "Bearer " + token
        headers= {'Authorization': bearer}
        uri = "https://api.mercadolibre.com/users/" + usuario
        response = requests.get(uri, headers=headers)
        nickname = response.text[response.text.find('"nickname":')+12:response.text.find(',',response.text.find('"nickname":'))-1]
        usuarios = Usuarios(nickname=nickname, usuario=usuario,token = token, refreshtoken = refreshtoken, tipo = 1, alta = dt.today(), baja = dt.today()+timedelta(days=15), palabrasminimas = 5,palabrasminimassi = False, tiempodeespera = 0, tiempodeesperasi = False, lunesnorespuesta = False, martesnorespuesta = False, miercolesnorespuesta = False, juevesnorespuesta = False, viernesnorespuesta = False, sabadonorespuesta = False, domingonorespuesta = False,  horainiciobloqueo = 8,  minutoiniciobloqueo = 30,  horafinbloqueo = 10, minutofinbloqueo = 30, bloqueotiemposi = False, bloqueadospreguntas = "", bloqueadoscompras = "", diarespuesta = "", horarespuesta = "", diamensaje = "", horamensaje = "",respuestasauto = 0,mensajesauto =0)
        print("1")
        usuarios.save()
        print("2")
        user = Usuarios.get_by_usuario(usuario).first()
        print("3")
        from models import Encrespuestas
        encrespuestas = Encrespuestas(user_id=usuario,encabezado = "", incluirencabezado = False, pie = "", incluirpie = False, palabrasmaximas = 5, palabrasmaximassi = False, palabrasprohibidas = "", reputacion = 0, borrarpregunta = False, bloquearusuario = False, palabrasprohibidassi = False, diasprohibidos = "", horainiciobloqueo=0,minutoiniciobloqueo=0, horafinbloqueo=0,minutofinbloqueo=0,bloqueotiemposi=False, unirrespuestas=False, respuestasunidas=0,unirrespuestaglobal=False)
        encrespuestas.save()
    else:
        user.token = token
        user.refreshtoken = refreshtoken
        user.save()
        nickname = user.nickname
    try:
        if user.baja < dt.today():
            return render_template('pagar.html', baja= user.baja)
        else:
            session['username'] = user.id
            nickname = user.nickname
            return redirect(url_for('perfil'))
    except AttributeError:
        usuarios = Usuarios(usuario=usuario,token = token, refreshtoken = refreshtoken, tipo = 1, alta = dt.today(), baja = dt.today()+timedelta(days=15), palabrasminimas = 5,palabrasminimassi = False, tiempodeespera = 0, tiempodeesperasi = False, lunesnorespuesta = False, martesnorespuesta = False, miercolesnorespuesta = False, juevesnorespuesta = False, viernesnorespuesta = False, sabadonorespuesta = False, domingonorespuesta = False,  horainiciobloqueo = 8,  minutoiniciobloqueo = 30,  horafinbloqueo = 10, minutofinbloqueo = 30, bloqueotiemposi = False, bloqueadospreguntas = "", bloqueadoscompras = "",mensajes = 0, respuestas = 0)
        usuarios.save()
        user = Usuarios.get_by_usuario(usuario).first()        
        print("4")
        print(user)
        if user.baja < dt.today():
            return render_template('pagar.html', baja= user.baja)
        else:
            session['username'] = user.id
            return render_template('perfil.html', user=user)        

@app.route("/clientes")
def clientes():
    return render_template('clientes.html')

@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/autorrespuestas", methods=["POST", "GET"])
def autorrespuestas():
    from models import Usuarios
    from models import Respuestas
    username = session['username']
    user = Usuarios.get_by_id(int(username))
    print("a")
    if request.method == 'POST':
        respuestas = Respuestas.get_by_global_user(int(username)).all()
        activos = []
        n = 0
        while n < 20:
            if request.form.get(str(n)) is not None:
                activos.append(n)
            n = n+1
        print(activos)
        print("activo")
        palabrasclaves = request.form.getlist('palabrasclave')
        respuestasb = request.form.getlist('respuesta')
        n=0
        print("b")
        for respuesta in respuestas:
            print(n)
            respuesta.palabrasclave = palabrasclaves[n]
            print()
            if n in activos:
                respuesta.activo = True
            else:
                respuesta.activo = False
                print("algo")
            respuesta.texto = respuestasb[n]
            n = n+1
            print("c")
            respuesta.save()
        if request.form.get('palabrasclavenuevo') != "" or request.form.get('respuestanuevo') != "":
            print("d")
            user_id = user.id
            palabrasclave = request.form.get('palabrasclavenuevo')
            texto = request.form.get('respuestanuevo')
            uso = 2
            activo = request.form.get('activonuevo')
            if activo == "on":
                activo = True
            respuesta = Respuestas(user_id=user_id,palabrasclave=palabrasclave,texto=texto,uso=uso,activo=activo)
            respuesta.save()
    respuestas = Respuestas.get_by_global_user(int(username)).all()
    print("e")
    listapalabras = []
    listarespuestas = []
    listaactivadas = []
    for respuesta in respuestas:
        print("f")
        listapalabras.append(respuesta.palabrasclave)
        listarespuestas.append(respuesta.texto)
        listaactivadas.append(respuesta.activo)
    print(listaactivadas)
    return render_template('autorrespuestas.html',user=user,listapalabras=listapalabras,listarespuestas=listarespuestas,listaactivadas=listaactivadas)

@app.route("/primermensaje")
def primermensaje():
    return render_template('primermensaje.html')

@app.route("/configurarmensajes")
def configurarmensajes():
    return render_template('configurarmensajes.html')

@app.route("/estadisticasmensajes")
def estadisticasmensajes():
    return render_template('estadisticasmensajes.html')

@app.route("/plantillas")
def plantillas():
    return render_template('plantillas.html')

@app.route("/postventa")
def postventa():
    return render_template('postventa.html')

@app.route("/especiales")
def especiales():
    return render_template('especiales.html')

@app.route("/masivos")
def masivos():
    listaProductos = ["producto1","producto2"]
    listaPrecios = ["precio1","precio2"]
    listaPermalink = ["link1","link2"]
    listaVendidos = ["vendidos1","vendidos2"]
    listaPictures = ["pictures1","pictures2"]
    listaStock =[]
    return render_template('masivos.html', productos=listaProductos,precios=listaPrecios,vendidos=listaVendidos,stock=listaStock,permalink=listaPermalink,pictures=listaPictures)

@app.route("/digitales")
def digitales():
    return render_template('digitales.html')

@app.route("/full")
def full():
    return render_template('full.html')

@app.route("/flex")
def flex():
    return render_template('flex.html')

@app.route("/preguntaspendientes", methods=["POST", "GET"])
def preguntaspendientes():
    from models import Sinrespuesta
    from models import Usuarios
    username = session['username']
    user = Usuarios.get_by_id(int(username))
    if request.method == 'POST':
        bearer = "Bearer " + user.token
        headers= {'Authorization': bearer}         
        uri = "https://api.mercadolibre.com/answers"                   
        seleccionados = request.form.getlist('select')
        if request.form['submit_button'] == 'Enviar respuestas':
            for cada in seleccionados:
                respuesta = request.form.get(cada)
                data = {"question_id": cada, "text":respuesta}
                requests.post(uri, json=data, headers=headers)
                sinrespuesta = Sinrespuesta.get_by_numero(cada).first()
                sinrespuesta.delete()
                # enviar un post donde cada es el codigo y respuesta el texto de la respuesta
        elif request.form['submit_button'] == 'No ver estas preguntas':
            for cada in seleccionados:
                sinrespuesta = Sinrespuesta.get_by_numero(cada).first()
                sinrespuesta.delete()
                # enviar un post donde cada es el codigo
        elif request.form['submit_button'] == 'Eliminar preguntas':
            for cada in seleccionados:
                uri = "https://api.mercadolibre.com/questions/" + cada
                sinrespuesta = Sinrespuesta.get_by_numero(cada).first()
                sinrespuesta.delete()
                requests.delete(uri, headers=headers)
                # enviar un post donde cada es el codigo
    sinrespuesta = Sinrespuesta.get_by_user(int(username)).all()
    lista = []
    listacodigo = []
    print(sinrespuesta)
    for sin in sinrespuesta:
        lista.append(sin.texto)
        listacodigo.append(sin.numero)
    return render_template('preguntaspendientes.html', user=user, lista=lista, listacodigo=listacodigo)

@app.route("/autorrespuestaglobal", methods=["POST", "GET"])
def autorrespuestaglobal():
    from models import Usuarios
    from models import Respuestas
    username = session['username']
    user = Usuarios.get_by_id(int(username))
    print("a")
    if request.method == 'POST':
        respuestas = Respuestas.get_by_unica_user(int(username)).first()
        if respuestas is not None:
            respuestas.texto = request.form.get('respuesta')
            if request.form.get('palabrasclave') == "on":
                respuestas.activo = True
            respuestas.save()
        else:
            user_id = user.id
            texto = request.form.get('respuesta')
            uso = 2
            if request.form.get('activo') == "on":
                activo = True
            else:
                activo = False
            respuesta = Respuestas(user_id=user_id,texto=texto,uso=uso,activo=activo)
            respuesta.save()
            print(activo)
            print(request.form.get('activo'))
    respuestas = Respuestas.get_by_unica_user(int(username)).first()
    if respuestas is not None:
        texto = respuestas.texto
        palabrasclave = respuestas.palabrasclave
        activo = respuestas.activo
    else:
        texto = ""
        palabrasclave = ""
        activo = False
    print("e")
    print("G")
    print(activo)
    return render_template('autorrespuestaglobal.html',user=user,texto=texto,activo=activo)

@app.route("/autorrespuestapubli", methods=["POST", "GET"])
def autorrespuestapubli():
    from models import Usuarios
    from models import Respuestas
    username = session['username']
    user = Usuarios.get_by_id(int(username))
    print("a")
    if request.method == 'POST':
        respuestas = Respuestas.get_by_pub_user(int(username)).all()
        activos = []
        n = 0
        while n < 20:
            if request.form.get(str(n)) is not None:
                activos.append(n)
            n = n+1
        palabrasclaves = request.form.getlist('palabrasclave')
        respuestasb = request.form.getlist('respuesta')
        pub_ids = request.form.getlist('publi')
        n=0
        print("b")
        for respuesta in respuestas:
            print(n)
            respuesta.palabrasclave = palabrasclaves[n]
            if n in activos:
                respuesta.activo = True
            else:
                respuesta.activo = False
                print("algo")
            respuesta.texto = respuestasb[n]
            respuesta.pub_id = pub_ids[n]
            print(pub_ids[n])
            n = n+1
            print("c")
            respuesta.save()
        if request.form.get('palabrasclavenuevo') != "" or request.form.get('respuestanuevo') != "":
            print("d")
            user_id = user.id
            palabrasclave = request.form.get('palabrasclavenuevo')
            texto = request.form.get('respuestanuevo')
            pub_id = request.form.get('publinuevo')
            uso = 3
            activo = request.form.get('activonuevo')
            if activo == "on":
                activo = True
            respuesta = Respuestas(user_id=user_id,pub_id =pub_id, palabrasclave=palabrasclave,texto=texto,uso=uso,activo=activo)
            respuesta.save()
    respuestas = Respuestas.get_by_pub_user(int(username)).all()
    print("e")
    listapalabras = []
    listarespuestas = []
    listaactivadas = []
    listacodigos = []
    for respuesta in respuestas:
        print("f")
        listapalabras.append(respuesta.palabrasclave)
        listarespuestas.append(respuesta.texto)
        listaactivadas.append(respuesta.activo)
        listacodigos.append(respuesta.pub_id)
    print("G")
    bearer = "Bearer " + user.token
    headers= {'Authorization': bearer}
    uri = "https://api.mercadolibre.com/users/" + user.usuario + "/items/search/"
    response = requests.get(uri, headers=headers)
    username = response.text + "xxx" + uri + "xxx" + bearer
    inicio = 0
    print(response.text)
    print(response.json()['results'])
    final = str(response.json()['results']).find(',',inicio)
    print(uri)
    print(response.text)
    print(bearer)
    print(username)
    n = 0 
    lista = []
    print(response.text)

    while n < 100:
        print("b")
        print(inicio)
        print(final)
        print(response.json()['results'][inicio:final-1])
        if final == -1:
            break
        if n == 0:
            lista.append(response.json()['results'][inicio:final])
        else:
            lista.append(response.json()['results'][inicio:final-1])
        inicio = final+2
        if inicio > len(response.json()['results']):
            break
        final = response.json()['results'].find(',',inicio+2) 
        n = n+1
    uri = "https://api.mercadolibre.com/items?ids="
    print("nueva uri es")
    print(uri)
    n = 0
    print("c")
    lista = response.json()['results']
    while n < len(lista):
        print("d")
        if n == 0:
            uri = uri + lista[n]
        else:
            uri = uri + "," + lista[n]
        n = n + 1
    print("e")
    print(uri)
    response = requests.get(uri, headers=headers)
    listaProductos = []
    n=0
    inicio = response.text.find('"title":')+9
    final = response.text.find('"',inicio+2)
    print(uri)
    while n < 10:
        print("f")
        if response.text[inicio:final-1] in listaProductos or uri == 'https://api.mercadolibre.com/items?ids=':
            break
        listaProductos.append(response.text[inicio:final-1])
        inicio = response.text.find('"title":',final)+9
        final = response.text.find('"',inicio+2)
        if inicio < 10:
            break
        n = n+1
    codigo = lista
    publicaciones = listaProductos
    publicaciones.insert(0,"")
    print(publicaciones)
    print(codigo)
    print(listacodigos)
    return render_template('autorrespuestapubli.html',codigo=codigo,publicaciones=publicaciones, user=user,listapalabras=listapalabras,listarespuestas=listarespuestas,listaactivadas=listaactivadas,listacodigos=listacodigos)

@app.route("/autorrespuestaconfi", methods=["POST", "GET"])
def autorrespuestaconfi():
    from models import Usuarios
    from models import Encrespuestas
    print("a")
    username = session['username']
    user = Usuarios.get_by_id(int(username))
    encrespuestas = Encrespuestas.get_by_user(user.usuario).first()
    print("a")
    if request.method == 'POST':
        print("b")
        seleccionados = request.form.getlist('select')
        diasprohibidos = ""
        print("c")
        for n in seleccionados:
            diasprohibidos = diasprohibidos + n + ","
        print(diasprohibidos)
        print("d")
        palabrasmaximas = request.form.get("palabrasmaximas")
        print("q")
        palabrasmaximassi = request.form.get('palabrasmaximassi')
        if palabrasmaximassi == "on":
            palabrasmaximassi = True
            print("cambiaso")
        print(palabrasmaximassi)
        palabrasprohibidas = request.form.get('palabrasprohibidas')
        print("e")
        borrarpregunta = request.form.get('borrarpregunta')
        if borrarpregunta == "on":
            borrarpregunta = True
        bloquearusuario = request.form.get('bloquearusuario')
        if bloquearusuario == "on":
            bloquearusuario = True
        palabrasprohibidassi = request.form.get('palabrasprohibidassi')
        if palabrasprohibidassi == "on":
            palabrasprohibidassi = True        
        horainiciobloqueo = request.form.get('horainiciobloqueo')
        minutoiniciobloqueo = request.form.get('minutoiniciobloqueo')
        horafinbloqueo = request.form.get('horafinbloqueo')
        minutofinbloqueo = request.form.get('minutofinbloqueo')
        bloqueotiemposi = request.form.get('bloqueotiemposi')
        if bloqueotiemposi == "on":
            bloqueotiemposi = True   
        unirrespuestas = request.form.get('unirrespuestas')
        if unirrespuestas == "on":
            unirrespuestas = True  
        respuestasunidas = request.form.get('respuestasunidas')
        unirrespuestaglobal = request.form.get('unirrespuestaglobal')
        if unirrespuestaglobal == "on":
            unirrespuestaglobal = True    
        print("requeridas")
        encrespuestas.palabrasmaximas = palabrasmaximas
        encrespuestas.palabrasmaximassi = palabrasmaximassi
        encrespuestas.palabrasprohibidas = palabrasprohibidas
        encrespuestas.borrarpregunta = borrarpregunta
        encrespuestas.bloquearusuario = bloquearusuario
        encrespuestas.palabrasprohibidassi = palabrasprohibidassi
        encrespuestas.diasprohibidos = diasprohibidos
        encrespuestas.horainiciobloqueo = horainiciobloqueo
        encrespuestas.minutoiniciobloqueo = minutoiniciobloqueo
        encrespuestas.horafinbloqueo = horafinbloqueo
        encrespuestas.minutofinbloqueo = minutofinbloqueo
        encrespuestas.bloqueotiemposi = bloqueotiemposi
        encrespuestas.unirrespuestas = unirrespuestas
        encrespuestas.respuestasunidas = respuestasunidas
        encrespuestas.unirrespuestaglobal = unirrespuestaglobal
        encrespuestas.save()
        print("e")
        print(encrespuestas.palabrasmaximassi)    
    split = encrespuestas.diasprohibidos.split(",")
    print(split)
    return render_template('autorrespuestaconfi.html',user=user,encrespuestas=encrespuestas,split=split)

@app.route("/autorrespuestametri")
def autorrespuestametri():
    return render_template('autorrespuestametri.html')

@app.route("/bloqueo")
def bloqueo():
    return render_template('bloqueo.html')

@app.route("/administrador")
def administrador():
    from models import Usuarios
    users= Usuarios.get_all()
    a = ""
    for usuario in users:
        a = a + str(usuario.usuario)
    return render_template('administrador.html', a=a)

@app.route("/notification",methods=["POST", "GET"])
def notification():
    print("uno")
    topic = request.json['topic']
    print("dos")
    if topic == "questions":
        print("tres")
        from respuestas import Preguntas
        preguntaid = request.json['resource'][11:]
        preguntauser= str(request.json['user_id'])
        Preguntas.preguntas(preguntaid,preguntauser)
    if topic == "messages":
        from respuestas import Mensaje
        mensajeid = request.json['resource']
        userid = request.json['user_id']
        Mensaje.mensajes(mensajeid,userid)
    if topic == "orders_v2":
        from respuestas import Orders
        orderid = request.json['resource'][8:]
        userid = str(request.json['user_id'])
        Orders.orders(orderid,userid)
    if topic == "payments":
        from respuestas import Pagos
        pagoid = request.json['resource'][13:]
        userid = request.json['user_id']
        Pagos.pagos(pagoid,userid)
    print("cuatro")
    return ("",200)











if __name__ == '__main__':
    app.run(debug=True)