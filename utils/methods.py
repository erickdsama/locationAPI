import functools
from datetime import datetime

import flask
from sqlalchemy.exc import IntegrityError

from models import Operator, User, Device, Location, Request

SECRET_KEY = 'develop'


def register_device(code, short_name, user, db_session=None):
    print "short_name", short_name
    print "code", code
    print "user", user.id

    device = Device(id_code=code, short_name=short_name, user=user.id)
    db_session.add(device)
    try:
        db_session.commit()
    except IntegrityError as e:
        raise e
    return device


def register_user(number, operator, db_session=None):
    operator = get_operator(operator)
    device = User(number=number, operator=operator.id)
    db_session.add(device)
    try:
        db_session.commit()
    except IntegrityError as e:
        raise e
    return device


def get_device(user_id=None, short_name=None, id_code=None):
    if id_code is not None:
        device = Device.query.filter(Device.id_code == id_code).first()
    else:
        device = Device.query.filter(Device.short_name == short_name).filter(Device.user == user_id).first()
    return device


def get_location(device):
    location = Location.query.filter(Location.device == device).order_by(Location.id.desc()).first()
    return location


def get_operator(operator_id):
    operator = Operator.query.filter(Operator.id == operator_id).first()
    return operator


def create_request(data, user):
    message = data.get("message")
    short_name = data.get("short_name")
    device = None
    if short_name:
        from sqlalchemy import and_
        device = Device.query.filter(and_(Device.user == user.id, Device.short_name == short_name)).first()
        device = device.id
    requester = Request(message=message, device=device, user=user.id, request_type='H', date_request=datetime.now().utcnow(), date_received=datetime.now().utcnow())
    requester.save()
    print requester
    return requester


def valid_user(f):
    @functools.wraps(f)
    def decorated_function(*args, **kws):
        data = flask.request.get_json() or flask.request.args
        if not data:
            flask.abort(403)
        else:
            print type(data)
            number = data.get("number")
            user = User.query.filter(User.number == number).first()
            if user is None:
                flask.abort(403)
            pending_request = create_request(data, user)
            return f(user, pending_request)

    return decorated_function


def add_request(device=None, user=None, db_session=None):
    request = Request(device=device, user=user)
    db_session.add(request)
    db_session.commit()
    return request


def set_location(lat=None, lng=None, device=None, db_session=None):
    location = Location(lat=lat, lng=lng, device=device)
    db_session.add(location)
    db_session.commit()
    return location
