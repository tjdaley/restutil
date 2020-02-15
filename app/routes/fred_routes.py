"""
fred_routes.py - Flask Routes for handling FRED requests.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from flask import Blueprint, request, jsonify
import app.util.util as UTIL
import app.services.fred as FRED

fred_routes = Blueprint('fred_routes', __name__, template_folder='templates')

@fred_routes('/fred/historical_rate/<int:year>/<int:month>/<int:term>/', methods=['GET'])
def get_historical_rate(year, month, term):
    fred_service = FRED.FredUtil()
    rate = fred_service.average_fixed_mortgage(year, month, term)
    params = {'year': year, 'month': month, 'term': term}
    data = {'query': 'historical_rate', 'params': params, 'response': rate}
    result = {'success': True, 'message': "OK", 'dataset': "FRED", 'data': data}
    return jsonify(result)
