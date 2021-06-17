from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import (
    validators,
    SubmitField,
    StringField,
    BooleanField
)


class FilterForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    enddate = DateField('End Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    chronological = BooleanField('Chronological')
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    search = StringField('Search')
    submit = SubmitField('Search')