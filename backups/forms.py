from flask_wtf import FlaskForm,Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired,Length, Email, EqualTo
class SearchForm(FlaskForm):
    playername= StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')




