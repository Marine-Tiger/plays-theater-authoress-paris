from ..app import app, db
from flask import render_template, request
from ..models.autrices import Play, Authoress, Theater
from ..models.formulaires import PlayForm, AddAuthoress
from sqlalchemy import create_engine, exc
from sqlalchemy.sql import text
from sqlalchemy import or_
from hashlib import md5
import os
from ..utils.transformations import  clean_arg

# ROUTE INSERTION D'UNE PIECE DE THEATRE
@app.route("/insertion/piece", methods=['GET', 'POST'])
def insertion_piece():
    form = PlayForm() 

    if form.validate_on_submit():
        name_authoress =  clean_arg(request.form.get("name_authoress", None))
        name_theater =  clean_arg(request.form.get("name_theater", None))
        url_AN =  clean_arg(request.form.get("url_AN", None))
        title =  clean_arg(request.form.get("title", None))

        # si un des champs est rempli
        if name_authoress or name_theater or url_AN or title:
            # si le champs name_authoress est rempli
            if name_authoress:
                # on verifie si le nom existe deja
                authoress_in_db = Authoress.query.filter(Authoress.id == name_authoress).all()
              
                # s'il n'existe pas, on peut creer la nouvelle autrice
                if not authoress_in_db:
                    print(authoress_in_db)
                    new_authoress = Authoress(id=name_authoress)
                    db.session.add(new_authoress)
                    db.session.commit()
                    print('Ca fonctionne')
                else:
                    print('Cette autrice existe déjà.')
        
            if name_theater:
                theater_in_db = Theater.query.filter(Theater.id_theater == name_theater).all()
                
                if not theater_in_db:
                    new_theater = Theater(id_theater=name_theater)
                    db.session.add(new_theater)
                    db.session.commit()
                else:
                    print('Ce théâtre existe déjà.')
            
            if title and url_AN:
                # md5 permet de hasher l'url_AN pour obtenir un id plus facilement manipulable par la machine (sans / dedans etc...)
                id_play = md5(url_AN.encode('utf-8')).hexdigest()
                # on verifie si l'id existe
                play_in_db = Play.query.filter(Play.url_AN == url_AN).all()
               
                if not play_in_db:
                    new_play = Play(url_AN=url_AN, title=title, id_play=id_play, authoress=name_authoress)
                    db.session.add(new_play)
                    db.session.commit()
                else:
                    print('Cette pièce existe déjà.')

    return render_template("partials/formulaires/insertion_piece.html", 
            sous_titre= "Insertion piece" , 
            form=form)


# ROUTE INSERTION D'UNE AUTRICE
@app.route("/insertion/autrice", methods=['GET', 'POST'])
def insertion_autrice():
    form = AddAuthoress()

    if form.validate_on_submit():
        name =  clean_arg(request.form.get("name", None))
        lien_wikipedia =  clean_arg(request.form.get("lien_wikipedia", None))
        id_wikidata =  clean_arg(request.form.get("id_wikidata", None))
        lien_bnf =  clean_arg(request.form.get("lien_bnf", None))

        authoress_in_db = Authoress.query.filter(Authoress.id == name).all()
        if not authoress_in_db: 
            new_authoress = Authoress(id=name, wikidata= id_wikidata, wikipedia=lien_wikipedia, bnf=lien_bnf)
            db.session.add(new_authoress)
            db.session.commit()
        else:
            print("Cette autrice existe déjà.")

    return render_template("partials/formulaires/insertions.html", 
            sous_titre= "Insertion autrice" , 
            form=form)
