from flask import render_template, g, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.forms import SignUpForm, SignInForm
from app.models import User
from app import app
from . import bp as auth

@app.before_request
def before_request():
    g.upform = SignUpForm()
    g.inform = SignInForm()

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    if g.inform.validate_on_submit():
        user = User.query.filter_by(email = g.inform.email.data).first()
        if user and user.check_password(g.inform.password.data):
            login_user(user)
            flash(f'{g.inform.email.data} logged in!')
            return redirect(url_for('main.home'))
        else:
            flash(f'Invalid User Data, Try Again')
        return redirect(url_for('main.home'))
    return render_template('signin.jinja', form = g.inform)

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    if g.upform.validate_on_submit():
        user_filter = User.query.filter_by(username=g.upform.username.data).first()
        email_filter = User.query.filter_by(email=g.upform.email.data).first()
        if user_filter or email_filter:
            flash(f"Username or Email already taken. Please Sign in <a href='signin'>here</a>.")
        else:
            user = User(username=g.upform.username.data, email=g.upform.email.data)
            user.hash_password(g.upform.password.data)
            user.set_score()
            user.commit()
            flash(f'{g.upform.username.data} registered')
            login_user(user)
            return redirect(url_for('main.home'))
    return render_template('signup.jinja', form = g.upform)

@auth.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('main.home'))