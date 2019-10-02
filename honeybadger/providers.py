import json
import requests
from flask import Blueprint, render_template, request, redirect, url_for
from honeybadger.auth import get_access_token, login_required
from honeybadger.mci import get_providers


bp = Blueprint('providers', __name__, url_prefix='/providers')


@bp.route('/')
@login_required
def index():
    providers = get_providers()
    return render_template('providers/index.html', providers=json.loads(providers))
