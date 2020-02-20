"""
fred_routes.py - Flask Routes for handling FRED requests.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import util.util as UTIL
import services.fred as FRED
from flask import Blueprint, request, jsonify

fred_routes = Blueprint('fred_routes', __name__, template_folder='templates')


@fred_routes.route('/fred/historical_rate/<int:year>/<int:month>/<int:term>/', methods=['GET'])
def get_historical_rate(year, month, term):
    fred_service = FRED.FredUtil()
    rate = fred_service.average_fixed_mortgage(year, month, term)
    params = {'year': year, 'month': month, 'term': term}
    data = {'query': 'historical_rate', 'params': params, 'response': rate}
    message = UTIL.success_message()
    message['dataset'] = 'FRED'
    message['data'] = data
    return jsonify(message)
