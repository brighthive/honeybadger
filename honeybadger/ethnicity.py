import json
import requests
from flask import Blueprint, render_template, request, redirect, url_for
from honeybadger.auth import get_access_token, login_required
from honeybadger.mci import get_ethnicities


bp = Blueprint('ethnicity', __name__, url_prefix='/ethnicity')


@bp.route('/')
@login_required
def index():
    ethnicities = get_ethnicities()
    return render_template('ethnicity/index.html', ethnicities=json.loads(ethnicities))
