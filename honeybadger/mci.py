import json
import requests
from math import ceil
from flask import Blueprint, render_template, request, redirect, url_for
from honeybadger.auth import get_access_token, login_required
from honeybadger.services import secure_get
from honeybadger.config import ConfigurationFactory


bp = Blueprint('mci', __name__, url_prefix='/mci')
config = ConfigurationFactory.from_env()


def get_genders():
    return secure_get(config.mci_url + '/gender', 'genders')


def get_ethnicities():
    return secure_get(config.mci_url + '/ethnicity', 'ethnicities')


def get_education_level():
    return secure_get(config.mci_url + '/education_level', 'education_levels')


def get_employment_status():
    return secure_get(config.mci_url + '/employment_status', 'employment_status')


def get_providers():
    return secure_get(config.data_resources_url + '/providers', 'providers')


@bp.route('/')
@login_required
def index():
    id = request.args.get('id')
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    if not offset or not limit:
        offset = 0
        query = '{}/users?offset={}'.format(config.mci_url, offset)
    else:
        query = '{}/users?offset={}&limit={}'.format(
            config.mci_url, offset, limit)
    token = get_access_token()
    headers = {'content-type': 'application/json',
               'authorization': 'bearer {}'.format(token)}
    r = requests.get(query, headers=headers)
    data = r.json()
    links = data['links']
    last_link = links[len(links) - 1]['href'].split('?')[1].split('&')

    # recalculate each time just in case
    _offset = int(last_link[0].split('=')[1])
    limit = int(last_link[1].split('=')[1])
    page_count = ceil(_offset / limit)
    current_page = ceil(int(offset) / limit) + 1
    if id:
        token = get_access_token()
        headers = {'content-type': 'application/json',
                   'authorization': 'bearer {}'.format(token)}
        query = '{}/users/{}'.format(config.mci_url, id)
        r = requests.get(query, headers=headers)
        if r.status_code == 200:
            user = r.json()

        # Clean the data for a bit more consistent output
        if len(user['education_level']) < 2:
            user['education_level'] = 'Unknown'
        user['gender'] = user['gender'].capitalize()
        ethnicities = get_ethnicities()
        ethnicity_count = len(ethnicities)
        return render_template('mci/index.html', users=data['users'], page_count=page_count, offset=int(offset), limit=limit, page=current_page, mode='CREATE', user=user)
    else:
        return render_template('mci/index.html', users=data['users'], page_count=page_count, offset=int(offset), limit=limit, page=current_page, mode='CREATE', user=None)


@bp.route('/users/<string:id>', methods=['GET'])
@login_required
def users(id: str):
    token = get_access_token()
    headers = {'content-type': 'application/json',
               'authorization': 'bearer {}'.format(token)}
    query = '{}/users/{}'.format(config.mci_url, id)
    r = requests.get(query, headers=headers)
    if r.status_code == 200:
        user = r.json()

    # Clean the data for a bit more consistent output
    if len(user['education_level']) < 2:
        user['education_level'] = 'Unknown'
    user['gender'] = user['gender'].capitalize()
    ethnicities = get_ethnicities()
    ethnicity_count = len(ethnicities)
    return render_template('mci/user_detail.html', user=user, mode='EDIT',
                           genders=get_genders(), ethnicities=ethnicities,
                           ethnicity_count=ethnicity_count, education_levels=get_education_level(),
                           employment_status=get_employment_status(), providers=get_providers())


@bp.route('/users/<string:id>/delete', methods=['GET'])
@login_required
def delete_user(id: str):
    token = get_access_token()
    headers = {'content-type': 'application/json',
               'authorization': 'bearer {}'.format(token)}
    query = '{}/users/{}'.format(config.mci_url, id)
    r = requests.delete(query, headers=headers)
    return redirect(url_for('mci.index'))
