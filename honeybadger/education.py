import json
import requests
from flask import Blueprint, render_template, request, redirect, url_for
from honeybadger.auth import get_access_token, login_required
from honeybadger.mci import get_education_level


bp = Blueprint('education', __name__, url_prefix='/education')


@bp.route('/')
@login_required
def index():
    education_levels = get_education_level()
    return render_template('education/index.html', education_levels=json.loads(education_levels))
