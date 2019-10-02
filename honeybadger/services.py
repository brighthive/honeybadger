"""Application Services

A collection of services for accessing external APIs.

"""

import os
import sys
import requests
import json

from honeybadger.config import ConfigurationFactory


def get_access_token():
    """ Retrieves an OAuth 2.0 access token from the OAuth 2.0 provider.

    Note:
        At present, we use Auth0 as our OAuth 2.0 provider.

    Returns:
        str: OAuth 2.0 access token.

    """

    config = ConfigurationFactory.from_env()
    headers = {'content-type': 'application/json'}
    data = {'client_id': config.client_id, 'client_secret': config.client_secret,
            'audience': config.audience, 'grant_type': 'client_credentials'}
    r = requests.post(config.oauth2_url, headers=headers,
                      data=json.dumps(data))
    return r.json()['access_token']


def secure_get(url: str, key: str = None):
    """Conveniene method for GET requests against API resources.

    Args:
        url (str): The URL for the GET request.
        key (str): The key to return from the resulting JSON object.

    Returns:
        dict: Results of the query if found.
        None: If no results found.

    """
    token = get_access_token()
    headers = {'content-type': 'application/json',
               'authorization': 'bearer {}'.format(token)}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        if key:
            return data[key]
        else:
            return data
    else:
        return None


def secure_post(url: str, data: dict, key: str = None):
    """Conveniene method for POST requests against API resources.

    Args:
        url (str): The URL for the POST request.
        data (dict): Request body to pass to JSON object.
        key (str): The key to return from the resulting JSON object.

    Returns:
        dict: Results of the query if found.
        None: If no results found.

    """
    token = get_access_token()
    headers = {'content-type': 'application/json',
               'authorization': 'bearer {}'.format(token)}
    print('Posting {}'.format(data))
    r = requests.post(url, headers=headers, data=json.dumps(data))
    if r.status_code == 200 or r.status_code == 201:
        if key:
            return r.json()[key]
        else:
            return r.json()
    else:
        return None


def secure_patch(url: str, data: dict, key: str = None):
    """Conveniene method for POST requests against API resources.

    Args:
        url (str): The URL for the PATCH request.
        data (dict): Request body to pass to JSON object.
        key (str): The key to return from the resulting JSON object.

    Returns:
        dict: Results of the query if found.
        None: If no results found.

    """
    token = get_access_token()
    headers = {'content-type': 'application/json',
               'authorization': 'bearer {}'.format(token)}
    r = requests.patch(url, headers=headers, data=json.dumps(data))
    if r.status_code == 200 or r.status_code == 201:
        if key:
            return r.json()[key]
        else:
            return r.json()
    else:
        return None


def secure_delete(url: str):
    """Conveniene method for DELETE requests against API resources.

    Args:
        url (str): The URL for the PATCH request.

    Returns:
        dict: Results of the query if found.
        None: If no results found.

    """
    token = get_access_token()
    headers = {'content-type': 'application/json',
               'authorization': 'bearer {}'.format(token)}
    r = requests.delete(url, headers=headers)
    if r.status_code == 200 or r.status_code == 201:
        return r.json()
    else:
        return None
