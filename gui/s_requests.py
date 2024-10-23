'''
make query to the server | api
'''

import requests
import json

def make_query(url:str, data_type:str=None,data:dict=None):
    """
    Make a query to the server using the specified URL and data.

    Args:
        url (str): The URL to make the query to.
        data (dict): A dictionary containing the data to be sent in the query.

    Returns:
        dict: Returns a dictionary containing the response from the server.
    """
    """ make query to server """
    try:
        if data_type == 'json':
            response = requests.post(url, json=data)
        elif data_type == 'params':
            response = requests.post(url, params=data)
        elif data_type == None:
            response = requests.post(url, data=json.dumps(data))
        response = requests.post(url, data=json.dumps(data))
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        return {'error': 'error'}
    ''''''
# username = 'admin'
# email = 'e@21'
# password = 'admin'
# _ = make_query('https://chat-app.fudemy.me/signup', {'username': username, 'email': email,'password': password})
# print(_)

