#Requires Log in, Sign up
#Search Bar to find Pokemon AND/OR users
#Add to add pokemon to pokedex
#Delete pokemon from pokedex
#Button for ability attack
#forfeit button
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo

class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('Your email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    reenter_password = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class SearchForm(FlaskForm):
    searchfield = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class BeginFightForm(FlaskForm):
    submit = SubmitField('Fight')

class ForfeitForm(FlaskForm):
    hidden = HiddenField()
    submit = SubmitField('Forfeit Fight')

class DeleteForm(FlaskForm):
    hidden = HiddenField()
    delete = SubmitField('Delete')

class ButtonForm(FlaskForm):
    submit = SubmitField()
