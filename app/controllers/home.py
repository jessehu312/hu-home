# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request

blueprint = Blueprint('home', __name__)

@blueprint.route('/')
def index():
    return render_template('home/client.html', **{'ip': request.remote_addr})
