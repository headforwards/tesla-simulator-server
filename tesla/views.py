from flask import render_template, Blueprint

blue_views = Blueprint('views', __name__)


@blue_views.route('/')
def index():
    return render_template('index.html')
