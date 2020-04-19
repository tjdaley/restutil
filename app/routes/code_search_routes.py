"""
code_search_routes.py - Flask Routes for handling Code Search requests.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import util.util as UTIL
import services.codesearch as CODE
from flask import Blueprint, request, jsonify
import urllib.parse

code_routes = Blueprint('code_routes', __name__, template_folder='templates')


@code_routes.route('/codesearch/search/<string:query>/<string:codelist>/', methods=['GET'])
def search_codified_laws(query, codelist):
    u_query = urllib.parse.unquote_plus(query)
    u_query = urllib.parse.unquote(u_query)
    u_codelist = urllib.parse.unquote_plus(codelist)
    u_codelist = urllib.parse.unquote(u_codelist)
    matches = CODE.search(u_query, u_codelist)
    return jsonify(matches)


@code_routes.route('/codesearch/list/', methods=['GET'])
def get_code_list():
    return jsonify(CODE.list_codes())
