"""
zillow_routes.py - Flask Routes for handling Zillow requests.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import util.util as UTIL
import services.zillow as ZILLOW
from flask import Blueprint, request, jsonify

zillow_routes = Blueprint('zillow_routes', __name__, template_folder='templates')


@zillow_routes.route('/zillow/value/<string:street>/<string:city_state_zip>', methods=['GET'])
def get_value(street, city_state_zip):
    zillow_service = ZILLOW.Zillow()
    parcel_info = zillow_service.search(street, city_state_zip)
    params = {'street': street, 'city_state_zip': city_state_zip}
    data = {'query': 'zillow/value', 'params': params, 'response': parcel_info}
    message = UTIL.success_message()
    message['dataset'] = 'ZILLOW'
    message['data'] = data
    return jsonify(message)
