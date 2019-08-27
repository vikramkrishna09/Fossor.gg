from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
class SearchForm(FlaskForm):
    playername= StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')
    playerregion = SelectField('region',choices=[('','Select a region'),('na1','Na'), ('euw1','Euw')],validators = [DataRequired()])



def validate_playerregion(form, field):
    if field.data == None:
        raise ValidationError('Please Select a region')

