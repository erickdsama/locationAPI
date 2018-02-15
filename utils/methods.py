from models import Operators, Users, Devices, Locations, Requests
from flask import session
import flask
import functools

SECRET_KEY = 'develop'

def get_device(user_id=None, short_name=None, id_code=None):
    if id_code is not None:
        device = Devices.query.filter(Devices.id_code == id_code).first()
    else:     
        device = Devices.query.filter(Devices.short_name == short_name).filter(Devices.user == user_id).first()
    return device
    

def get_location(device):
    location = Locations.query.filter(Locations.device == device).first()
    return location

def get_operator(operator_id):
    operator = Operators.query.filter(Operators.id == operator_id).first()
    return operator

def valid_user(f):
    @functools.wraps(f)
    def decorated_function(*args, **kws):
        data = flask.request.get_json()
        print data, "?"
        if not data:
            flask.abort(403)
        else:
            number = data.get("number")
            user = Users.query.filter(Users.number == number).first()
            if user is None:
                flask.abort(403)
            return f(user)
    return decorated_function

def add_request(device=None, user=None, db_session=None):
    request = Requests(device=device, user=user)
    db_session.add(request)
    db_session.commit()
    return request

def set_location(lat=None, lng=None, device=None, db_session=None):
    location = Locations(lat=lat, lng=lng, device=device)
    db_session.add(location)
    db_session.commit()
    return location

