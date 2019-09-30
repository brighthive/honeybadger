import json
import requests
from math import ceil
from flask import Blueprint, render_template, request, redirect, url_for
from honeybadger.auth import get_access_token, login_required
from honeybadger.config import ConfigurationFactory
from honeybadger.services import secure_get, secure_post


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
    return render_template('referrals/index.html', referrals=referrals['referrals'], offset=int(offset), page=current_page,
                           limit=limit, page_count=page_count, last_offset=last_offset)


@bp.route('/<string:id>', methods=['GET'])
@login_required
def get_referrals(id):
    if id:
        query = '{}/referrals/query'.format(config.data_resources_url)
        data = {'mci_id': id}
        referrals = secure_post(query, data, 'results')
    else:
        query = '{}/referrals'
        referrals = secure_get(query, 'results')
    return render_template('referrals/index.html', referrals=referrals, page=1)
