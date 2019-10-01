import json
import requests
from flask import Blueprint, render_template, request, redirect, url_for
from honeybadger.auth import get_access_token, login_required
from honeybadger.mci import get_employment_status


bp = Blueprint('employment', __name__, url_prefix='/employment')


@bp.route('/')
@login_required
def index():
    employment_statuses = get_employment_status()
    return render_template('employment/index.html', employment_statuses=json.loads(employment_statuses))
