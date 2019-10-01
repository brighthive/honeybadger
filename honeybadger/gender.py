import json
import requests
from flask import Blueprint, render_template, request, redirect, url_for
from honeybadger.auth import get_access_token, login_required
from honeybadger.mci import get_genders


bp = Blueprint('gender', __name__, url_prefix='/gender')


@bp.route('/')
@login_required
def index():
    genders = get_genders()
    return render_template('gender/index.html', genders=json.loads(genders))
