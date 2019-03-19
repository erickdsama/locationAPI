from flask import Flask
from flask import jsonify
from flask import request

from models.Users import User
from utils.database import db_session, init_db
from utils.methods import *

init_db()
app = Flask(__name__)


@app.route('/get_location', methods=['POST', 'GET'])
@valid_user
def api_get_location(user):
    data_form = request.get_json()
    short_name = data_form.get("short_name")
    device = get_device(user_id=user.id, short_name=short_name)
    print "device", device
    location = get_location(device.id)
    print "location", location
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
                "id": user.id,
                "number": user.number,
                "operator": {
                    "id": operator.id,
                    "number": operator.number
                }
            }
        }
    }
    return jsonify(data)

@app.route('/register_user', methods=['POST'])
def api_register_user():
    data_form = request.get_json()
    number = data_form.get("number")
    operator = data_form.get("operator")
    print "number=", number
    try:
        user = User.query.filter(User.number == number).first()
        if user is not None:
            return jsonify({"error": "numero ya registrado"}), 409

        user = register_user(number, operator, db_session)
        # device = register_device(code=id_code, short_name=short_name, user=user, db_session=db_session)
    except IntegrityError:
        return jsonify({"error": "id_code ya registrado"}), 409
    except KeyError as e:
        return jsonify({"error": "no esta definido: {}".format(e)}), 400
    except Exception as e:
        return jsonify({"error": "{}".format(e)}), 400
    return jsonify(user.to_dict()), 201


@app.route('/register_device', methods=['POST'])
@valid_user
def api_register_device(user):
    data_form = request.get_json()
    id_code = data_form.get("id_code")
    short_name = data_form.get("short_name")
    try:
        device = register_device(code=id_code, short_name=short_name, user=user, db_session=db_session)
    except IntegrityError:
        return jsonify({"error": "id_code ya registrado"}), 409
    except KeyError as e:
        return jsonify({"error": "no esta definido: {}".format(e)}), 400
    except Exception as e:
        return jsonify({"error": "{}".format(e)}), 400
    return jsonify(device.to_dict()), 201

@app.route('/set_location', methods=['POST', 'GET'])
def api_set_location():
    data_form = request.get_json()
    id_code = data_form.get("id_code")
    lat = data_form.get("lat")
    lng = data_form.get("lng")
    # id_code = "8dkjsa9dask"

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
