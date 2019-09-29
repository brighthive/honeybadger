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
    query = '{}/referrals'.format(config.data_resources_url)
    referrals = secure_get(query, 'referrals')
    return render_template('referrals/index.html', referrals=referrals, page=1, limit=20, page_count=20)


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
