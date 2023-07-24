from app import login_manager, db
from flask_login import UserMixin
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

def check_index(arr, i):
    try:
        test = arr[i]
        return True
    except:
        return False

#User needs ID, username, email, password(hashed), pokemon relationship, leaderboard score, battle relationship
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    email = db.Column(db.String(80), nullable = False, unique = True)
    pass_hash = db.Column(db.String(), nullable = False)
    score = db.Column(db.Integer)
    joined = db.Column(db.DateTime, default = date.today())
    my_poke = db.relationship('Pokemon', backref = 'trainer', lazy = True, foreign_keys="Pokemon.user_id")
    my_f = db.relationship('Battle', backref = 'fighter', lazy = True, foreign_keys="Battle.f_user_id")
    my_d = db.relationship('Battle', backref = 'defender', lazy = True, foreign_keys="Battle.d_user_id")   

    def __repr__(self):
        return f'USER: {self.username}'
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
    
    def get_id(self):
        return str(self.user_id)
    
    def hash_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)
    
    def from_dict(self, d):
        self.username  = d['username']
        self.email  = d['email']
        self.pass_hash  = d['password']
        self.hash_password(self.pass_hash)  

    def to_dict(self):
        d = {
            'user_id' : self.user_id,
            'username' : self.username,
            'email' : self.email,
            'rank' : self.score,
            'joined' : self.joined
        }
        return d
    
    def raise_rank(self):
        if self.score == 1:
            return
        else:
            self.score -= 1

    def set_score(self):
        rank = User.query.count() + 1

    def update_rank(self):
        if self.rank > User.query.count():
            self.set_score()


#Pokemon needs ID, name, level, health, front sprite, back sprite, type1, type2, user relationship, move1,  move2,  move3,  move4   
class Pokemon(db.Model):
    poke_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    level = db.Column(db.Integer, default = 1, nullable = False)
    health = db.Column(db.Integer, default = 12, nullable = False)
    first_type = db.Column(db.String(20), nullable = False)
    second_type = db.Column(db.String(20), nullable = True)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.user_id'), nullable = False)
    move1 = db.Column(db.String(20), nullable = False)
    move2 = db.Column(db.String(20), nullable = True)
    move3 = db.Column(db.String(20), nullable = True)
    move4 = db.Column(db.String(20), nullable = True)
    fr_sprite = db.Column(db.String(100), nullable = False)
    bk_sprite = db.Column(db.String(100), nullable = False)
    battle_f = db.relationship('Battle', backref = 'poke_fighter', lazy = True, foreign_keys = 'Battle.f_pokemon_id')
    battle_d = db.relationship('Battle', backref = 'poke_defender', lazy = True, foreign_keys = 'Battle.d_pokemon_id')


    def __repr__(self):
        return f'{self.name}'
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_pokemon(self):
        db.session.delete(self)
        db.session.commit()

    def raise_level(self):
        self.level += 1
        self.health += 2

    def to_dict(self):
        d = {}
        return d

    def from_dict(self , d):
        self.name = d['name']
        self.first_type = d['types'][0]['type']['name']
        self.user_id = current_user.user_id
        self.move1 = d['moves'][0]['move']['name']
        self.fr_sprite = d['sprites']['front_default']
        self.bk_sprite = d['sprites']['back_default']
        if check_index(d['moves'], 1):
            self.move2 = d['moves'][1]['move']['name']
        if check_index(d['moves'], 2):
            self.move3 = d['moves'][2]['move']['name']
        if check_index(d['moves'], 3):
            self.move4 = d['moves'][3]['move']['name']
        if check_index(d['types'], 1):
            self.second_type = d['types'][1]['type']['name']



#Battle class needs ID, fighter relationship, defender relationship, pokemon fighter relationship, pokemon defender relationship, 
# turn, pokemon fighter health,  pokemon defender health
class Battle(db.Model):
    battle_id = db.Column(db.Integer, primary_key = True)
    f_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    d_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    f_pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.poke_id'), nullable = False)
    d_pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.poke_id'), nullable = False)
    f_health = db.Column(db.Integer, nullable = False)
    d_health = db.Column(db.Integer, nullable = False)
    turn = db.Column(db.Integer, default = 0, nullable = False)

    def __init__(self, d_user, f_poke, d_poke):
        self.f_user = current_user
        self.d_user = d_user
        self.f_pokemon = f_poke
        self.d_pokemon = d_poke
        self.f_health = f_poke.health
        self.d_health = d_poke.health
        self.turn = 0

    def __repr__(self):
        return f"{self.f_user.username} vs. {self.d_user.username} - {self.f_pokemon.name} vs. {self.d_pokemon.name}"

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_battle(self):
        db.session.delete(self)
        db.session.commit()


