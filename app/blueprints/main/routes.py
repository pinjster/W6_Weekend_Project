from flask import render_template, redirect, url_for, g, request, flash
from flask_login import login_required, current_user
from app.forms import SearchForm
from . import bp as main
from app import app

@main.route('/', methods = ['GET', 'POST'])
def home():
    if 'signin' in request.form:
        return redirect(url_for('auth.signin'))
    elif 'signup' in request.form:
        return redirect(url_for('auth.signup'))
    return render_template('index.jinja', form_poke = SearchForm())
