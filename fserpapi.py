#unused files
"""
API functions file
Every method returns a list with a boolean and JSON or String of error
"""

from requests import get, put, post, ConnectionError

import json

# need a config file or should get it
HOST = 'http://localhost:8800'
HEADERS = {'Content-type': 'application/json'}
PARAMS = {'key': '123', 'password': '12453'}


def get_dish_categories():
    """
    get dish categories
    """
    try:
        response = get(HOST + '/dish/categories/',
                       data=json.dumps(PARAMS), headers=HEADERS)
        return True, response.content
    except ConnectionError:
        return False, 'No Connection'


def add_dish_category(dish, parent=None):
    """
    add dish categories
    :param dish: the new dish category name
    :param parent: the parent category
    """
    localparams = PARAMS.copy()
    localparams.update({'name': dish, 'parent': parent})
    try:
        response = put(HOST + '/dish/category/',
                       data=json.dumps(localparams), headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'


def get_ingredients():
    """
    get dish ingredients
    """
    try:
        response = get(HOST + '/ingredients/',
                       data=json.dumps(PARAMS), headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'


def get_ingredient_categories():
    """
    get dish ingredient categories
    """
    try:
        response = get(HOST + '/ingredients/categories/',
                       data=json.dumps(PARAMS), headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'


def ingredient_add(ingredient, parent=None):
    """
    add dish ingredient
    :param ingredient: the new ingredient name
    :param parent: the parent category of the ingredient
    """
    localparams = PARAMS.copy()
    localparams.update({'name': ingredient, 'parent': parent})
    try:
        response = put(HOST + '/ingredient/',
                       data=json.dumps(localparams), headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'


def add_ingredients_category(category, parent=None):
    """
    add dish ingredient category
    :param category: the new ingredient category name
    :param parent: the parent category of the ingredient
    """
    localparams = PARAMS.copy()
    localparams.update({'name': category, 'parent': parent})
    try:
        response = put(HOST + '/ingredients/category/',
                       data=json.dumps(localparams), headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'


def get_messages_updates():
    """
    get message updates
    """
    try:
        response = get(HOST + '/messages/updates/',
                       data=json.dumps(PARAMS), headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'


def get_message(msgid):
    """
    get message updates of the id
    :param msgid: the message id
    """
    try:
        response = get(HOST + '/messages/',
                       params={'id': int(msgid)},
                       data=json.dumps(PARAMS), headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'


def get_employee_designations():
    """
    get employee designations
    """
    try:
        response = get(HOST + '/employee/designations/',
                       data=json.dumps(PARAMS), headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'


def get_designation(design_id):
    """
    gets the employee designation of the passed id
    :param design_id: the id of the designation
    """
    try:
        response = get(HOST + '/employee/designation/',
                       params={'id': int(design_id)}, data=json.dumps(PARAMS),
                       headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'


def get_billing_last():
    """
    get last bill
    """
    try:
        response = get(HOST + '/billing/last/',
                       data=json.dumps(PARAMS), headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'


def get_billing_summary():
    """
    get billing summary
    """
    try:
        response = post(HOST + '/billing/summary/',
                        data=json.dumps(PARAMS), headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'


def get_company_departments():
    """
    get company departments
    """
    try:
        response = get(HOST + '/company/departments/',
                       data=json.dumps(PARAMS), headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'


def get_inventory_summary():
    """
    get inventory summary
    """
    try:
        response = post(HOST + '/invetory/summary/',
                        data=json.dumps(PARAMS), headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'


def get_inventory_last():
    """
    get last inventory
    """
    try:
        response = get(HOST + '/invetory/last/',
                       data=json.dumps(PARAMS), headers=HEADERS)
        return response.content
    except ConnectionError:
        return False, 'No Connection'

# """
# @app.put('/company/department/')
# """

# from bottle import route
#
# route?
# route?
# % edit
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# from bottle import redirect
#
# redirect?
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# from bottle.ex
# import bottle.ext
#
# dir(bottle.ext)
# bottle.ext.__all__
# impoer
# bottle_mysql
# import bottle_mysql
# import bottle_mysq;
# import bottle_mysql
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# % edit / tmp / ipython_edit_dzYKrA.py
# from requests import put
# import json
#
# json?
# d = {'key': 123, 'password': 567}
# put?
# ret = put('http://localhost:8800/dish/categories/', data=d)
# ret = put('http://localhost:8800/dish/categories/', data=d)
# ret = put('http://localhost:8800/dish/categories/', data=d)
# ret
# ret = put('http://localhost:8800/dish/categories/', data=d)
# ret.content
# ret = put('http://localhost:8800/dish/category/', data=d)
# ret
# put?
# ret = put('http://localhost:8800/dish/category/', data=d)
# ret = put('http://localhost:8800/dish/category/', data=d)
# d = {'key': 123, 'password': 567, 'name': 'Rice'}
# ret = put('http://localhost:8800/dish/category/', data=d)
# ret
# ret = put('http://localhost:8800/dish/category/', data=d)
# ret
# ret.content
# from requests import get
#
# ret = get('http://localhost:8800/dish/category/')
# ret
# ret = get('http://localhost:8800/dish/categories/')
# ret
# ret.content
# ret = get('http://localhost:8800/ingredients/')
# ret.content
# ret = get('http://localhost:8800/ingredients/')
# d = {'key': 123, 'password': 567, 'name': 'Rice'}
# ret.headers
# ret = get('http://localhost:8800/dish/category/', data=d)
# ret
# ret.content
# ret.content
# ret = put('http://localhost:8800/dish/category/', data=d)
# from bottle import request
# from bottle import request as req
#
# req.json?
# ret
# ret = put('http://localhost:8800/dish/category/', data=d)
# ret = put('http://localhost:8800/dish/category/', data=d)
# ret.headers
# put?
# ret = put('http://localhost:8800/dish/category/', data=d, {'content-type': 'application/json'})
# ret = put('http://localhost:8800/dish/category/', data=d, {'content-type' = 'application/json'})
# ret = put('http://localhost:8800/dish/category/', data=d, {'content-type': 'application/json'})
# ret = put('http://localhost:8800/dish/category/', data=d, 'content-type' = 'application/json')
# ret = put('http://localhost:8800/dish/category/', data=d, {'content-type': 'application/json'})
# ret = put('http://localhost:8800/dish/category/', data=d, 'content-type' = 'application/json')
# headers = {'content-type': 'application/json'}
# ret = put('http://localhost:8800/dish/category/', data=d, headers)
# put?
# ret = put('http://localhost:8800/dish/category/', headers, data=d)
# ret = put('http://localhost:8800/dish/category/', data=d, headers)
# put?
# ret = put('http://localhost:8800/dish/category/', data=d, headers)
# d.update(headers)
# ret = put('http://localhost:8800/dish/category/', data=d)
# ret
# ret.content
# ret = put('http://localhost:8800/dish/category/', data=d)
# ret = put('http://localhost:8800/dish/category/', data=d)
# ret.headers
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d))
# ret.headers
# ret.content
# ret.content
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d))
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d))
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d))
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d))
# ret.headers
# ret.headers
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d))
# headers = {'Content-type': 'application/json'}
# d.update(headers)
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d))
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d))
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d))
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d))
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d))
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d), headers=headers)
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d), headers=headers)
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d), headers=headers)
# ret.content
# ret = put('http://localhost:8800/dish/category/', data=d, headers=headers)
# ret = put('http://localhost:8800/dish/category/', data=json.dumps(d), headers=headers)
#
