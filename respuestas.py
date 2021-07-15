from datetime import datetime as dt
import requests

class Convertir:
    def convertir(texto):
        texto = texto
        return texto

class Preguntas:
    def preguntas(numero,userid):
        from models import Usuarios
        from models import Preguntas
        from models import Encrespuestas
        user = Usuarios.get_by_usuario(userid).first()
        print("PRUEBA SUPERADAPRUEBA SUPERADAPRUEBA SUPERADAPRUEBA SUPERADA")
        config = Encrespuestas.get_by_user(userid).first()
        print(config)
        bearer = "Bearer " + user.token
        headers= {'Authorization': bearer}
        uri = "https://api.mercadolibre.com/questions/" + numero
        response = requests.get(uri, headers=headers)
        print(response.text)
        if response.json()['status'] == 404:
            return ("",200)
        texto = response.json()['text']
        publicacion = response.json()['item_id']
        responder = True
        if config.palabrasmaximassi:
            if config.palabrasmaximas < texto.count(" "):
                from models import Sinrespuesta
                nueva = Sinrespuesta(user_id = user.id, pub_id = publicacion, texto=texto, numero=numero)
                responder = False
        if config.palabrasprohibidassi and responder:
            lista = config.palabrasprohibidas.split(",")
            prohibida = False
            for palabra in lista:
                if texto.count(" " + palabra +" ") > 0:
                    if config.borrarpregunta:
                        uri = "https://api.mercadolibre.com/questions/" + numero
                        requests.delete(uri, headers=headers)
                    else:
                        nueva = Sinrespuesta(user_id = user.id, pub_id = publicacion, texto=texto, numero=numero)
                        nueva.Save()
                    prohibida = True
                    responder = False
                    break
        if config.bloqueotiemposi and responder:
            bloqueado = False
            lista = config.diasprohibidos.split(",")
            if dt.now().weekday() in lista:
                if dt.now().hour() > config.horainiciobloqueo and dt.now().hour() < config.horafinbloqueo:
                    nueva = Sinrespuesta(user_id = user.id, pub_id = publicacion, texto=texto, numero=numero)
                    nueva.Save()
                    responder = False
                elif dt.now().hour() == config.horainiciobloqueo and dt.now().minute() > config.minutoiniciobloqueo:
                    nueva = Sinrespuesta(user_id = user.id, pub_id = publicacion, texto=texto, numero=numero)
                    nueva.Save()
                    responder = False
                elif dt.now().hour() == config.horafinbloqueo and dt.now().minute() < config.minutofinbloqueo:
                    nueva = Sinrespuesta(user_id = user.id, pub_id = publicacion, texto=texto, numero=numero)
                    nueva.Save()
                    responder = False
        if responder:
            respuesta = ""
            n = 0
            from models import Respuestas
            publi = Respuestas.get_by_pub_id(publicacion).first()
            if publi is not None:
                if publi.uso == 4:
                    if publi.activo:
                        respuesta = respuesta + Convertir.convertir(texto)(publi.texto)
                        headers= {'Authorization': bearer, 'content-type': 'application/json'}
                        data = {"question_id": numero, "text":respuesta}
                        uri = "https://api.mercadolibre.com/answers"
                        response = requests.post(uri, json=data, headers=headers)
                        responder = False
                elif publi.uso == 3:
                    if publi.activo:
                        respuesta = respuesta + Convertir.convertir(publi.texto)
                    n = n+1
        if responder:
            publi = Respuestas.get_by_unica_user(user.id).first()
            if publi is not None:
                if publi.activo:
                    respuesta = respuesta + Convertir.convertir(publi.texto)
                    headers= {'Authorization': bearer, 'content-type': 'application/json'}
                    data = {"question_id": numero, "text":respuesta}
                    uri = "https://api.mercadolibre.com/answers"
                    response = requests.post(uri, json=data, headers=headers)
                    responder = False
        if responder:
            unir = Respuestas.get_by_palabra_user(user.id, texto).all()
            if unir is not None:
                for una in unir:
                    if una.activo:
                        respuesta = respuesta + Convertir.convertir(una.texto)
                    n = n+1
                    if config.respuestasunidas < n:
                        break
            unir = Respuestas.get_by_global_user(user.id).first()
            if unir is not None and config.respuestasunidas >= n:
                if unir.activo:
                    respuesta = respuesta + Convertir.convertir(unir.texto)
            if respuesta != "":
                headers= {'Authorization': bearer, 'content-type': 'application/json'}
                data = {"question_id": numero, "text":respuesta}
                uri = "https://api.mercadolibre.com/answers"
                response = requests.post(uri, json=data, headers=headers)
                responder = False
        if responder:
            from models import Sinrespuesta
            nueva = Sinrespuesta(user_id = user.id, pub_id = publicacion, texto=texto, numero=numero)
            nueva.save()


#class Mensaje(numero,userid):

#class Orders(numero,userid):

#class Pagos(numero,userid):