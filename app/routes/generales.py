from ..app import app, db
from flask import render_template, request
from ..models.autrices import Play, Authoress, Theater
from ..models.formulaires import PlayForm
from sqlalchemy import create_engine, exc
from sqlalchemy.sql import text
from sqlalchemy import or_
import os
from ..utils.transformations import  clean_arg

@app.route("/home", methods=["GET","POST"])
def home():
    name = []
    for name_authoress in Authoress.query.all():
        name.append(name_authoress.id)
    return name

# creation de la route vers une page de presentation des autrices 
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
    
