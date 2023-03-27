from ..app import app, db
import uuid

# #table de relation configuration(forme) et play (la piece)
play_configuration = db.Table(
    "play_configuration",
    db.Column('id_configuration', db.Text, db.ForeignKey('configuration.id_configuration'), primary_key=True),
    db.Column('id_play', db.Text, db.ForeignKey('play.id_play'), primary_key=True)
)

#table de relation theatre(lieux) et play (la piece)
play_theater = db.Table(
    "play_theater",
    db.Column('id_theater', db.Text, db.ForeignKey('theater.id_theater'), primary_key=True),
    db.Column('id_play', db.Text, db.ForeignKey('play.id_play'), primary_key=True)
)

#table de relation type(genres) et play (la piece)
play_type = db.Table(
    "play_type",
    db.Column('id_type', db.String(100), db.ForeignKey('type.id_type'), primary_key=True),
    db.Column('id_play', db.Text, db.ForeignKey('play.id_play'), primary_key=True)
)

# Table de la piece de theatre
class Play(db.Model):
    #on peut nommer la table autre que le nom de la classe, permet de changer plus facilement
    __tablename__ = "play"
    #db.Text = pas de nombres de caracteres predefinis // db.String on definit la longueur de la chaine de caracteres
    id_play = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    date = db.Column(db.Integer)
    is_published = db.Column(db.Integer)
    digitized = db.Column(db.Text)
    authoress = db.Column(db.Text, db.ForeignKey('authoress.id'))
    other_author = db.Column(db.Text)

    Authoress = db.relationship(
        'Authoress',
        backref='Authoress',
        lazy=True
    )


     # Jointure many-to-many
    configuration = db.relationship(
        'Configuration',
        secondary= play_configuration,
        backref='configuration'                              
    )

    theater = db.relationship(
        'Theater',
        secondary = play_theater,
        backref = 'theater'
    )

    type = db.relationship(
        'Type',
        secondary = play_type,
        backref = 'type'
    )

class Configuration(db.Model):
    __tablename__ = "configuration"
    id_configuration = db.Column(db.Text, primary_key=True)


class Theater(db.Model):
    __tablename__ = "theater"
    id_theater = db.Column(db.Text, primary_key=True)


class Type(db.Model):
    __tablename__ = "type"
    id_type = db.Column(db.Text, primary_key=True)

# Table pour les autrices
class Authoress(db.Model):
    __tablename__ = "authoress"
    id = db.Column(db.Text, primary_key=True)
    wikidata = db.Column(db.Text, nullable=True)
    wikipedia = db.Column(db.Text, nullable=True)
    bnf = db.Column(db.Text, nullable=True)
