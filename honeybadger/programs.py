import json
import requests
from flask import Blueprint, render_template, request, redirect, url_for
from honeybadger.auth import get_access_token, login_required
from honeybadger.mci import get_programs


bp = Blueprint('programs', __name__, url_prefix='/programs')


@bp.route('/')
@login_required
def index():
    programs = get_programs()
    return render_template('programs/index.html', programs=json.loads(programs))
