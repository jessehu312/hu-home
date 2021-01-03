from app.models.family import Family
from flask import Blueprint, render_template, request

blueprint = Blueprint('home', __name__)

@blueprint.route('/')
def index():
    families = Family.query.all()
    family = None
    if families:
        family = families[0]
    return render_template('home/client.html', **{'ip': request.remote_addr, 'familyId': family.id})
