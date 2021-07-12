"""
ms_addin_routes.py - Flask Routes for handling requests from Microsoft Add-Ins

Copyright (c) 2021 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import util.util as UTIL
from flask import Blueprint, request, jsonify

ms_routes = Blueprint('ms_addin_routes', __name__, template_folder='templates')


@ms_routes.route('/objection_responses', methods=['GET'])
def get_get_objection_responses():
    doc = [
        {'key': 'obj_relevance', 'content': "This is relevant.", 'label': "Relevance"},
        {'key': 'obj_fishing', 'content': "Go fish.", 'label': "Fishing Expedition"},
        {'key': 'obj_overbroad', 'content': "Is it really over broad?", 'label': "Over Broad"},
    ]

    responses = {i['key']: i for i in doc}

    return jsonify(responses)
