from requests import get
from . import bp as api

call = "https://pokeapi.co/api/v2/pokemon/"

@api.route('/get-pokemon/<pokename>', methods=['GET', 'POST'])
def get_pokemon(pokename):
    try:
        info = get(f"https://pokeapi.co/api/v2/pokemon/{pokename.lower()}")
        if info.ok:
            return info.json()
    except:
        return None