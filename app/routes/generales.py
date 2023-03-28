from ..app import app, db
from flask import render_template, request
from ..models.autrices import Play, Authoress, play_theater, Theater, Configuration, Type, play_configuration, play_type
from ..models.formulaires import PlayForm
from sqlalchemy import create_engine, exc
from sqlalchemy.sql import text
from sqlalchemy import or_, and_
import os
from ..utils.transformations import  clean_arg

@app.route("/home", methods=["GET","POST"])
def home():
    name = []
    for name_authoress in Authoress.query.order_by(Authoress.id).all():
        name.append(name_authoress.id)
    return name

# PAGE DE PRESENTATION DES AUTRICES
@app.route("/presentation_autrice/<string:name>")
def presentation(name):
    data= db.session.query(Authoress, Play)\
    .join(Play.Authoress).\
    filter(Authoress.id == name).all()
    id_authoress = {}

    # Python ne sait pas comment transformer une instance de classe en json car impossible 
    # (une instance de classe peut contenir des fonctions/attributs prives/publics = pas representable en json)
    # ==> on transf la donnee en dict que python sait serialiser (transfo) en json (donc en donnees les unes a la suite des autres)

    # creation d'une variable autrice qui stocke l'elmt[0] la tuple
    autrice=data[0][0]
    # on ajoute au dictionnaire une clef dont la valeur est le 1er elmt de la tuple
    # pour transformer l'elmt en dictionnaire, on accede a sa propriete via le .[propriete] ==> propriete qui est un string ici
    id_authoress['authoress'] = {
        'id': autrice.id, 
        'wikipedia': autrice.wikipedia, 
        'wikidata': autrice.wikidata,
        'bnf': autrice.bnf
    }

    # Pour ajouter les proprietes de la classe Play
    # La clef 'piece' a pour valeur une liste
    id_authoress['piece'] =  [
    ]
    
    for elm in data:
        # une variable piece qui vaut la position une dans la tuple
        piece=elm[1]
        # a chaque tour, on ajoute a la liste les differents elements de la table Play
        id_authoress['piece'].append({'cote_AN':piece.id_play, 
                                      'titre':piece.title, 
                                      'date': piece.date, 
                                      'autre auteur': piece.other_author, 
                                      'lien numerisation':piece.digitized,
                                      'publié': piece.is_published == 1})
    print(id_authoress)
    return id_authoress


# PAGE DES PIECES DE THEATRE
@app.route("/liste_pieces")
def liste_piece():
    piece = []
    for titre_piece in Play.query.order_by(Play.title).all():
        piece.append((titre_piece.title, titre_piece.id_play))
    return piece
# PAGE POUR CHAQUE PIECE
@app.route("/liste_pieces/<string:titre>")
def presentation_piece(titre):
    # J'effectue une requete SQLAlchemy pour recuperer les informations des tables Play, Configuration, Theater et Type 
    # en faisant un .join avec les jointures declarees dans la class Play
    data= db.session.query(Play)\
    .select_from(Play)\
    .join(Play.configuration)\
    .join(Play.theater)\
    .join(Play.type)\
    .filter(Play.title == titre).all()
    # Je renvoie vers la template
    return render_template ('pages/liste_pieces_titre.html',
                            # pour pouvoir utiliser les resultats contenus dans data qui est une liste, 
                            # je cree une variable piece qui va contenir la liste de l'ensemble des informations requêtées
                            # même si je sais qu'il n'y a qu'une seule piece, je suis obligee de le preciser avec le [0] 
                            # car la machine ne le sait pas
                            piece = data[0],
                            titre = titre)

    # print(data[0].theater.id_theater)
    # return {
    #     'play_number': len(data),
    #     'theater': data[0].theater[0].id_theater,
    #     'configuration': data[0].configuration[0].id_configuration,
    #     'type': data[0].type[0].id_type
    # }
    # piece=data[0][0]
    # print(piece)
    # id_piece['play']={
    #     'title': piece.title,
    #     'url_AN': piece.id_play,
    #     'date': piece.date,
    # }

    



    
