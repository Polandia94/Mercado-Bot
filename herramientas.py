from datetime import datetime as dt
from flask import redirect, url_for

def chequearUsuario(user):
    if user.baja < dt.today():
        return redirect(url_for('pagar'))