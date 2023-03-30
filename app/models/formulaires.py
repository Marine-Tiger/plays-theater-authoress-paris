from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SelectField
from wtforms.validators import InputRequired
from. autrices import Type

class AddAuthoress(FlaskForm):
    name = StringField('name_authoress', validators=[])
    lien_wikipedia = StringField('title_play', validators=[])
    id_wikidata = StringField('id_play', validators=[])
    lien_bnf = StringField('name_theater', validators=[])

class AddPlay(FlaskForm):
    # fonction pour permettre de selectionner en valeurs de SelectField la table Type
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type.choices = [
            (el.id_type) for el in Type.query.all()
        ]
    type = SelectField("type", coerce=str)
    title = StringField('title_play', validators=[InputRequired()])
    url_AN = StringField('id_play', validators=[InputRequired()])
    date = StringField('date', validators=[])
    name_authoress = StringField('name_authoress', validators=[InputRequired()])
    other_author = StringField('other_author', validators=[])
    name_theater = StringField('name_theater', validators=[])
    configuration = StringField('configuratoin', validators=[])
    is_published = StringField('is_published', validators=[])
    digitized = StringField('digitized', validators=[])

class Update(FlaskForm):
    name_authoress = StringField('new_name_authoress', validators=[])
    new_name_authoress = StringField('new_name_authoress', validators=[])
    lien_wikipedia = StringField('title_play', validators=[])
    id_wikidata = StringField('id_play', validators=[])
    lien_bnf = StringField('name_theater', validators=[])
    new_url_AN = StringField('id_play', validators=[])
    new_title_play = StringField('title_play', validators=[])
    new_date = IntegerField('date', validators=[])
    new_is_published = StringField('is_published', validators=[])
    new_digitized = IntegerField('digitized', validators=[])
    new_other_author = StringField('new_other_author', validators=[])

class AjoutUtilisateur(FlaskForm):
    prenom = StringField("prenom", validators=[])
    password = PasswordField("password", validators=[])

class Connexion(FlaskForm):
    prenom = StringField("prenom", validators=[])
    password = PasswordField("password", validators=[])