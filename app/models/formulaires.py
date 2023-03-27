from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField

class PlayForm(FlaskForm):
    title = StringField('title_play', validators=[])
    url_AN = StringField('id_play', validators=[])
    name_authoress = StringField('name_authoress', validators=[])
    name_theater = StringField('name_theater', validators=[])

class Update(FlaskForm):
    name_authoress = StringField('name_authoress', validators=[])
    new_name_authoress = StringField('new_name_authoress', validators=[])
    url_AN = StringField('id_play', validators=[])
    new_url_AN = StringField('id_play', validators=[])
    title_play = StringField('title_play', validators=[])
    new_title_play = StringField('title_play', validators=[])
    date = IntegerField('date', validators=[])
    new_date = IntegerField('date', validators=[])
    is_published = StringField('is_published', validators=[])
    new_is_published = StringField('is_published', validators=[])
    digitized = IntegerField('digitized', validators=[])
    new_digitized = IntegerField('digitized', validators=[])
    other_author = StringField('other_author', validators=[])
    new_other_author = StringField('other_author', validators=[])