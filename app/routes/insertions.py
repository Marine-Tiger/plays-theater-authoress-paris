from ..app import app, db
from flask import render_template, request
from ..models.autrices import Play, Authoress, Theater
from ..models.formulaires import PlayForm
from sqlalchemy import create_engine, exc
from sqlalchemy.sql import text
from sqlalchemy import or_
import os
from ..utils.transformations import  clean_arg

# ROUTE INSERTION
@app.route("/insertions/piece", methods=['GET', 'POST'])
def insertion_piece():
    form = PlayForm() 

    if form.validate_on_submit():
        name_authoress =  clean_arg(request.form.get("name_authoress", None))
        name_theater =  clean_arg(request.form.get("name_theater", None))
        url_AN =  clean_arg(request.form.get("url_AN", None))
        title =  clean_arg(request.form.get("title", None))

        # si un des champs est rempli
        if name_authoress or name_theater or url_AN or title:
            print(url_AN, title)
            # si le champs name_authoress est rempli
            if name_authoress:
                # on verifie si le nom existe deja
                authoress_in_db = Authoress.query.filter(Authoress.id == name_authoress).all()
                print(authoress_in_db)
                # s'il n'existe pas, on peut creer la nouvelle autrice
                if not authoress_in_db:
                    new_authoress = Authoress(id=name_authoress)
                    db.session.add(new_authoress)
                    db.session.commit()
                    print('Ca fonctionne')
                else:
                    print('Cette autrice existe déjà.')
        
            if name_theater:
                theater_in_db = Theater.query.filter(Theater.id_theater == name_theater).all()
                print(theater_in_db)
                if not theater_in_db:
                    new_theater = Theater(id_theater=name_theater)
                    db.session.add(new_theater)
                    db.session.commit()
                else:
                    print('Ce théâtre existe déjà.')
            
            if title and url_AN:
                # on verifie si l'id existe
                play_in_db = Play.query.filter(Play.id_play == url_AN).all()
                print(play_in_db)
                if not play_in_db:
                    new_play = Play(id_play=url_AN, title=title, authoress=name_authoress)
                    db.session.add(new_play)
                    db.session.commit()
                else:
                    print('Cette pièce existe déjà.')

    return render_template("partials/insertion_piece.html", 
            sous_titre= "Insertion piece" , 
            form=form)