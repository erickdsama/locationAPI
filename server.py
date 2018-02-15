import os
import time 

from datetime import datetime

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask_marshmallow import Marshmallow

from utils.methods import *
from utils.database import db_session, init_db
from sqlalchemy import extract, desc

init_db()
app = Flask(__name__)

@app.route('/get_location', methods=['POST', 'GET'])
@valid_user
def api_get_location(user):
    data_form = request.get_json()
    short_name = data_form.get("short_name")
    device = get_device(user_id=user.id, short_name=short_name)
    location = get_location(device.id)
    operator = get_operator(user.operator)

    request_set = add_request(device=device.id, user=user.id, db_session=db_session)

    data = {
        "id": location.id,
        "lat": location.lat,
        "lng": location.lng,
        "date": location.date_registered,
        "device": {
            "id": device.id, 
            "short_name": device.short_name, 
            "tag": device.id_code,
            "user": {
                "id":user.id,
                "number":user.number,
                "operator": {
                    "id":operator.id,
                    "number":operator.number
                }
            }
        }
    }
    return jsonify(data)

@app.route('/set_location', methods=['POST', 'GET'])
def api_set_location():
    data_form = request.get_json()
    id_code = data_form.get("id_code")
    lat = data_form.get("lat")
    lng = data_form.get("lng")
    id_code = "8dkjsa9dask"

    device = get_device(id_code=id_code)
    location_sets = set_location(lat=lat, lng=lng, device=device.id, db_session=db_session)
    data = {
        "id": location_sets.id,
        "lat": location_sets.lat,
        "lng": location_sets.lng,
        "date": location_sets.date_registered,
        "device": {
            "id": device.id, 
            "short_name": device.short_name, 
            "tag": device.id_code
        }
    }
    return jsonify(data)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()