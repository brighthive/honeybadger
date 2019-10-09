import json
import requests
from math import ceil
from flask import Blueprint, render_template, request, redirect, url_for
from honeybadger.auth import get_access_token, login_required
from honeybadger.config import ConfigurationFactory
from honeybadger.services import secure_get, secure_post, secure_patch, secure_delete
from honeybadger.logger import logger


bp = Blueprint('referrals', __name__, url_prefix='/referrals')
config = ConfigurationFactory.from_env()


@bp.route('/', methods=['GET'])
@login_required
def index():
    offset = request.args.get('offset')
    limit = request.args.get('limit')

    # note this is a fix for the error with miscalcuation of offsets for pages beyond 1
    last_offset = request.args.get('last_offset')

    if not offset or not limit:
        offset = 0
        query = '{}/referrals?offset={}'.format(
            config.data_resources_url, offset)
    else:
        query = '{}/referrals?offset={}&limit={}'.format(
            config.data_resources_url, offset, limit)
    referrals = secure_get(query)
    links = referrals['links']
    try:
        last_link = links[len(links) - 1]['href'].split('?')[1].split('&')

        # recalculate each time just in case
        if not last_offset:
            _offset = int(last_link[0].split('=')[1])
        else:
            _offset = int(last_offset)
        limit = int(last_link[1].split('=')[1])
        page_count = ceil(_offset / limit)
        current_page = ceil(int(offset) / limit) + 1
        if current_page == 1:
            last_offset = _offset
    except Exception:
        logger.warn('Failed to compute pagination')
        last_offset = 0
        current_page = 0
        page_count = 0
        offset = 0
    return render_template('referrals/index.html', referrals=referrals['referrals'], offset=int(offset), page=current_page,
                           limit=limit, page_count=page_count, last_offset=last_offset)


@bp.route('/<string:id>', methods=['GET'])
@login_required
def get_referral(id):
    query = '{}/referrals/{}'.format(config.data_resources_url, id)
    referral = secure_get(query)
    return json.dumps(referral)


@bp.route('/query/<string:id>', methods=['GET'])
@login_required
def query_referral(id):
    data = {'mci_id': id}
    query = '{}/referrals/query'.format(config.data_resources_url)
    resp = secure_post(query, json.dumps(data), 'results')
    user_query = '{}/users/{}'.format(config.mci_url, id)
    user_resp = secure_get(user_query)
    try:
        return render_template('referrals/index.html', referrals=resp, offset=0, page=1, limit=1, page_count=0, last_offset=0, user=user_resp)
    except Exception:
        return render_template('referrals/index.html', referrals=[], offset=0, page=1, limit=1, page_count=0, last_offset=0, user=user_resp)


@bp.route('/<string:id>', methods=['POST'])
@login_required
def service_referral(id):
    data = request.json
    query = '{}/referrals/{}'.format(config.data_resources_url, id)
    resp = secure_patch(query, data)
    return json.dumps({'message': 'OK!'})


@bp.route('/', methods=['POST'])
@login_required
def create_referral():
    data = request.json
    query = '{}/referrals'.format(config.data_resources_url)
    resp = secure_post(query, json.dumps(data))
    return json.dumps({'message': 'OK!'})


@bp.route('/<string:id>', methods=['DELETE'])
@login_required
def delete_referral(id):
    data = request.json
    query = '{}/referrals/{}'.format(config.data_resources_url, id)
    resp = secure_delete(query)
    return json.dumps({'message': 'OK!'})
