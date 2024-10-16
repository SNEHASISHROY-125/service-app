'''
make query to the server | api
'''

import requests
import json

def make_query(url, data):
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
        response = requests.post(url, data=json.dumps(data))
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        return {'error': 'error'}
    ''''''
username = 'admin'
email = 'e@21'
password = 'admin'
_ = make_query('https://chat-app.fudemy.me/signup', {'username': username, 'email': email,'password': password})
print(_)

