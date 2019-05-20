import sys

import requests
from flask import Flask
from flask import jsonify
from flask import request

from utils.database import db_session, init_db
from utils.methods import *

init_db()
app = Flask(__name__)


@app.route('/location', methods=['GET'])
@valid_user
def api_get_location(user, pending_request):
    try:
        device = pending_request.device
        if not device:
            raise Exception("Dispositivo no encontrado")

        location = Location.query.filter(Location.device == device).first()
        if not location:
            raise Exception("No hay ubicaciones registradas")
        response = "http://maps.google.com/maps?q={},{}&z=17".format(location.lat, location.lng)
        pending_request.response = response
        pending_request.status = 'T'
        pending_request.date_request = datetime.now().utcnow()
        pending_request.save()
        return jsonify({}), 200
    except Exception as e:
        pending_request.status = 'F'
        pending_request.response = str(e)
        pending_request.date_request = datetime.now().utcnow()
        pending_request.save()
        return jsonify({"error": str(e)}), 400

@app.route('/user', methods=['POST'])
def api_register_user():
    data_form = request.get_json()
    number = data_form.get("number")
    operator = data_form.get("operator")
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
def api_register_device():
    data_form = request.get_json()
    print("*"*200)
    print("DATA FORM ", data_form)
    sys.stdout.flush()

    id_code = data_form.get("id_code")
    short_name = data_form.get("short_name")
    number = data_form.get("number")
    operator = data_form.get("operator")

    try:

        try:
            user = register_user(number, operator, db_session)
        except IntegrityError:
            return jsonify({"error": "id_code ya registrado"}), 409

        try:
            device = register_device(code=id_code, short_name=short_name, user=user, db_session=db_session)
        except IntegrityError:
            return jsonify({"error": "id_code ya registrado"}), 409
        except KeyError as e:
            return jsonify({"error": "no esta definido: {}".format(e)}), 400

    except Exception as e:
        return jsonify({"error": "{}".format(e)}), 400
    return jsonify(device.to_dict()), 201

"""
AT+CSTT="CMNET"
AT+CIICR
AT+HTTPPARA="CID",1
AT+CIFSR
AT+CIPSTART="TCP","19f765e7.ngrok.io/"
AT+HTTPPARA="URL","http://19f765e7.ngrok.io/location"
AT+HTTPPARA="URL","http://19f765e7.ngrok.iolocation"
AT+HTTPPARA="CONTENT","application/json"


AT+HTTPDATA=150,15000
{"lat":"30.4050", "lng": "-130.42323", "id_code":"Ax34b9"}
AT+HTTPACTION=1


"""
@app.route('/location', methods=['POST'])
def api_set_location():
    ugly_data = str(request.get_data())
    print("ugly_data", ugly_data)
    start = ugly_data.find("{")
    end = ugly_data.find("}")
    str_json = ugly_data[start:end+1]
    import json
    data_form = json.loads(str_json)
    # data_form = request.get_data()
    id_code = data_form.get("id_code")
    lat = data_form.get("lat")
    lng = data_form.get("lng")
    # id_code = "8dkjsa9dask"
    device = Device.query.filter(Device.id_code == id_code).first()
    # device = get_device(id_code=id_code)
    if not device:
        raise Exception("Device not registered")
    # data_form["date_registered"] =
    data_form.pop("id_code")
    data_form["device"] = device.id
    location = Location(**data_form)
    location.save()
    # location_sets = set_location(lat=lat, lng=lng, device=device.id, db_session=db_session)
    # data = {
    #     "id": location_sets.id,
    #     "lat": location_sets.lat,
    #     "lng": location_sets.lng,
    #     "date": location_sets.date_registered,
    #     "device": {
    #         "id": device.id,
    #         "short_name": device.short_name,
    #         "tag": device.id_code
    #     }
    # }
    return jsonify({})


@app.route('/help', methods=['GET'])
@valid_user
def help(user, pending_request):
    try:
        data = {
            "message":
                """
Hola! Gracias por pedir ayuda.
Te explicare de manera sencilla como usar el sistema

Esta es una lista de opciones:
-dispositivos
-ayuda
-registrar qr_id [nombre]
-[nombre_dispositivo] para buscar

                """
        }
        pending_request.status = 'T'
        pending_request.response = data.get("message")
        pending_request.date_request = datetime.now().utcnow()
        pending_request.save()
        return jsonify(data)
    except Exception as e:
        print("error", e)
        pending_request.status = 'F'
        pending_request.response = "Estamos en mantenimiento, espera unos segundos"
        pending_request.date_request = datetime.now().utcnow()
        pending_request.save()
        return jsonify({"error": str(e)}), 400


@app.route('/available_devices', methods=['GET'])
@valid_user
def available_devices(user, pending_request):
    try:
        devices = Device.query.filter(Device.user == user.id).all()
        devices_names = [device.short_name for device in devices]
        devices_obj = {
            "devices": devices_names
        }
        pending_request.status = 'E'
        pending_request.response = "{}".format(devices_obj)
        pending_request.date_request = datetime.now().utcnow()
        pending_request.save()
        return jsonify(devices_obj), 200
    except Exception as e:
        print("error", e)
        pending_request.status = 'F'
        pending_request.response = "Error en el servidor {}".format(e)
        pending_request.date_request = datetime.now().utcnow()
        pending_request.save()
        return jsonify({"error": str(e)}), 400


@app.route('/request', methods=['GET'])
# @valid_user
def get_messages_to_send():
    try:
        to_send = Request.query.filter(Request.status == 'T').all()

        if not to_send:
            return jsonify({}), 404
        data = []  # type: [Request]

        for message in to_send:
            user = User.query.filter(User.id == message.user).first()
            message.status = "E"
            # Operator
            message_obj = {
                "number": "521{}@s.whatsapp.net".format(user.number),
                "message": message.response,
            }
            message.save()
            data.append(message_obj)

        return jsonify(data), 200
    except Exception as e:
        print("error", e)
        # pending_request.status = 'F'
        # pending_request.response = "Error en el servidor {}".format(e)
        # pending_request.date_request = datetime.now().utcnow()
        # pending_request.save()
        return jsonify({"error": str(e)}), 400


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


#if __name__ == '__main__':
#    app.run(debug=True)
