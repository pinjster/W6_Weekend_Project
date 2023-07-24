from flask import redirect, url_for, render_template, g, request, flash
from flask_login import login_required
from app.forms import SearchForm
from app.models import User
from app import app
from . import bp as fight

@app.before_request
def before_request():
     g.usf = SearchForm()

@fight.route('/fight/<username>')
@login_required
def fight_user():
    pass

@fight.route('/search-profile/<username>')
@login_required
def search_profile(username):
    user = User.query.filter_by(username=username).first()
    userlist = User.query.all()
    return render_template('search_profile.jinja', user = user, form = g.usf, userlist = userlist)
    
@fight.post('/usersearch')
def usersearch():
    return redirect(url_for('fight.search_profile', username = g.usf.searchfield.data))