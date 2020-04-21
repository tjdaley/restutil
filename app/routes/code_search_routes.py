"""
code_search_routes.py - Flask Routes for handling Code Search requests.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import redis
import json
import util.util as UTIL
import services.codesearch as CODE
from flask import Blueprint, request, jsonify
import urllib.parse

code_routes = Blueprint('code_routes', __name__, template_folder='templates')


redis_service = redis.Redis(
    host=UTIL.get_env('REDIS_HOST', 'localhost'),
    port=int(UTIL.get_env('REDIS_PORT', 6379)),
    db=0
)


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
    """
    Get a list of codified laws and their searchability flags.
    This is a very slow function call because for each code configuration we find,
    we query the index to see if there are any documents indexed into that code
    section. To avoid doing that check every time, we cache the response and use
    the cached response for every query for the next 30 minutes.

    First, see if we have a cached response. If so, use it.
    Otherwise, get a new response and cache it for 30 minutes.
    """
    key = '/codesearch/list/'
    listing = redis_service.get(key)
    if listing:
        listing_list = json.loads(listing)
    else:
        listing_list = CODE.list_codes()
        redis_service.set(key, json.dumps(listing_list))
        redis_service.expire(key, 30*60)  # expire every 30 minutes
    return jsonify(listing_list)
