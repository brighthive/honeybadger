import json
import requests
from math import ceil
from flask import Blueprint, render_template, request, redirect, url_for
from honeybadger.auth import get_access_token, login_required
from honeybadger.mci import get_programs, get_providers, get_genders, get_ethnicities, get_education_level, get_employment_status
from honeybadger.config import ConfigurationFactory


bp = Blueprint('home', __name__, url_prefix='/')
config = ConfigurationFactory.from_env()


def compute_mci_records():
    token = get_access_token()
    headers = {'content-type': 'application/json',
               'authorization': 'bearer {}'.format(token)}
    query = '{}/users?offset={}'.format(config.mci_url, 0)
    r = requests.get(query, headers=headers)
    data = r.json()
    links = data['links']
    last_link = links[len(links) - 1]['href'].split('?')[1].split('&')

    # recalculate each time just in case
    _offset = int(last_link[0].split('=')[1])
    limit = int(last_link[1].split('=')[1])
    page_count = ceil(_offset / limit)
    query = '{}/users?offset={}&limit={}'.format(
        config.mci_url, _offset, limit)
    r = requests.get(query, headers=headers)
    last_page = len(r.json()['users'])
    total = (page_count * limit) + last_page
    return total


def compute_referral_records():
    token = get_access_token()
    headers = {'content-type': 'application/json',
               'authorization': 'bearer {}'.format(token)}
    query = '{}/referrals?offset={}'.format(config.data_resources_url, 0)
    r = requests.get(query, headers=headers)
    data = r.json()
    links = data['links']
    last_link = links[len(links) - 1]['href'].split('?')[1].split('&')

    # recalculate each time just in case
    _offset = int(last_link[0].split('=')[1])
    limit = int(last_link[1].split('=')[1])
    page_count = ceil(_offset / limit)
    query = '{}/referrals?offset={}&limit={}'.format(
        config.data_resources_url, _offset, limit)
    r = requests.get(query, headers=headers)
    last_page = len(r.json()['referrals'])
    total = (page_count * limit) + last_page
    return total


@bp.route('/')
@login_required
def index():
    stats = []
    data_resources = ['Master Client Index', 'Referrals', 'Programs', 'Providers',
                      'Gender', 'Ethnicity and Race', 'Education Level', 'Employment Status']

    for data_resource in data_resources:
        if data_resource == 'Programs':
            data = json.loads(get_programs())
        elif data_resource == 'Providers':
            data = json.loads(get_providers())
        elif data_resource == 'Gender':
            data = json.loads(get_genders())
        elif data_resource == 'Ethnicity and Race':
            data = json.loads(get_ethnicities())
        elif data_resource == 'Education Level':
            data = json.loads(get_education_level())
        elif data_resource == 'Employment Status':
            data = json.loads(get_employment_status())
        elif data_resource == 'Master Client Index':
            data = compute_mci_records()
        elif data_resource == 'Referrals':
            data = compute_referral_records()
        else:
            data = None
        if data:
            if isinstance(data, list):
                resource_stat = {
                    'data_resource': data_resource,
                    'status': 'OK',
                    'record_count': len(data) if data else 0
                }
            else:
                resource_stat = {
                    'data_resource': data_resource,
                    'status': 'OK',
                    'record_count': data
                }
        else:
            resource_stat = {
                'data_resource': data_resource,
                'status': 'Fail',
                'record_count': 0
            }
        stats.append(resource_stat)

    return render_template('home/index.html', stats=stats)
