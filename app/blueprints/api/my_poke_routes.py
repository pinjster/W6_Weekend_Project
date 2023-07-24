from flask import jsonify, request, url_for
from requests import get
from flask_login import login_required
from app.models import Pokemon, User
from . import bp as api

@api.post('/add-pokemon/<username>')
@login_required #temporary
def api_add_pokemon(username):
    user = User.query.filter_by(username = username).first()
    if not user:
        return jsonify(status= "Username does not exist")
    info = request.json
    url = request.url_root
    poke = get(f"{url}{url_for('api.get_pokemon', pokename = info['name'])}"), 400
    if poke.ok:
        data = poke.json()
        new_poke = Pokemon()
        new_poke.from_dict(data)
        return jsonify(status= f"Pokemon {info['name']} added to {user.username}'s Pokedex"), 200
    else:
        return jsonify(status= f"Pokemon {info['name']} not valid"), 400
    
@api.delete('/delete-pokemon/<poke_id>')
@login_required #temporary
def api_delete_pokemon(poke_id):
    poke = Pokemon.query.filter_by(poke_id = poke_id).first()
    if not poke:
        return jsonify(status= "Pokemon does not exist"), 400
    else:
        poke.delete_pokemon()
        return jsonify(status= f"{poke.name} has been removed"), 200
    


