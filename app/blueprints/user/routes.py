from flask_login import login_required, current_user
from flask import flash, render_template, url_for, redirect
from app.models import Pokemon, User
from . import bp as user


@user.route('/delete-pokemon/<poke_id>', methods=['POST', 'GET'])
@login_required 
def delete_pokemon(poke_id):
    poke = Pokemon.query.filter_by(poke_id = poke_id).first()
    me = User.query.filter_by(user_id = current_user.user_id).first()
    if poke in me.my_poke:
        flash(f"Deleted the pokemon {poke.name}")
        poke.delete_pokemon()
    else:
        flash('Cannot delete this pokemon')
    return redirect(url_for('user.profile'))

@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.jinja', user = current_user)