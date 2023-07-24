from flask import g, redirect, render_template, url_for, request, flash
from flask_login import login_required, current_user
from requests import get
from app.models import Pokemon, User
from app.forms import SearchForm
from app import app
from . import bp as find

@app.before_request
def before_request():
      g.usf = SearchForm()

@find.route('/find-pokemon/<poke_name>', methods = ['GET', 'POST'])
@login_required
def find_pokemon(poke_name):
    url = request.url_root
    poke = get(f"{url}{url_for('api.get_pokemon', pokename = poke_name)}")
    if poke.ok:
        data = poke.json()
        new_poke = Pokemon()
        new_poke.from_dict(data)
    else:
        new_poke = None
    if f'{new_poke.poke_id}' in request.form:
        new_poke.commit()
        flash(f'{new_poke.trainer.username} caught a {new_poke.name}!')
        return redirect(url_for('main.home'))
    return render_template('search_pokemon.jinja', poke = new_poke, form = g.usf)

@find.post('/pokesearch')
@login_required
def pokesearch():
    return redirect(url_for('find.find_pokemon', poke_name = g.usf.searchfield.data))