from flask import Blueprint, render_template

# auth.py already redirected to 'main.index' after login and logout, but no
# blueprint by that name was ever registered, so both routes raised a
# BuildError. index.html existed with nothing serving it.
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')
