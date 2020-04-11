"""
code_search_routes.py - Flask Routes for handling Code Search requests.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import util.util as UTIL
import services.codesearch as CODE
from flask import Blueprint, request, jsonify

code_routes = Blueprint('code_routes', __name__, template_folder='templates')


@code_routes.route('/codesearch/<string:query>/<string:codelist>/', methods=['GET'])
def get_historical_rate(query, codelist):
    code_searcher = CODE.CodeSearch()
    matches = code_searcher.search(query, codelist)
    return jsonify(matches)
