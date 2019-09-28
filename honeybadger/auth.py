"""Auth Module.

Handles all authorization and authentication concerns.

"""

import os
import json
import requests

from flask import Blueprint, redirect, url_for, g, render_template, session, request
from functools import wraps

from honeybadger.services import get_access_token
from honeybadger.config import ConfigurationFactory

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    """View decorator that redirects unknown users to a simple login page."""

    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    name = session.get('name')
    if name:
        g.user = name
    else:
        g.user = None


@bp.route('/login')
def login():
    if g.user:
        return redirect(url_for('mci.index'))
    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    g.user = None
    return redirect(url_for('auth.login'))


@bp.route('/callback')
def oauth2_callback():
    code = request.args.get('code')
    config = ConfigurationFactory.from_env()
    if code:
        data = {'client_id': config.github_client_id,
                'client_secret': config.github_client_secret,
                'code': code}
        headers = {'content-type': 'application/json',
                   'accept': 'application/json'}
        r = requests.post(config.github_oauth2_url,
                          headers=headers, data=json.dumps(data))
        token = r.json()['access_token']
        headers = {'content-type': 'application/json',
                   'authorization': 'token {}'.format(token)}
        r = requests.get(config.github_profile_url, headers=headers)
        session['name'] = r.json()['name']
        return redirect(url_for('home.index'))
    return redirect(url_for('auth.login'))
