import json
import requests
from flask import Blueprint, render_template, request, redirect, url_for
from honeybadger.auth import get_access_token, login_required


bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
@login_required
def index():
    return render_template('home/index.html')
