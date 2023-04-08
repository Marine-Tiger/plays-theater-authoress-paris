from ..app import app, db
from flask import render_template, request, flash
from flask_login import login_required
from ..models.autrices import Play, Authoress, Theater, Type, Configuration,play_configuration, play_theater, play_type
from ..models.formulaires import AddPlay, AddAuthoress
from sqlalchemy import create_engine, exc
from sqlalchemy.sql import text
from sqlalchemy import or_
from hashlib import md5
import os
from ..utils.transformations import  clean_arg

# ROUTE INSERTION D'UNE PIECE DE THEATRE
@app.route("/insertion/piece", methods=['GET', 'POST'])
@login_required
def insertion_piece():
    form = AddPlay() 
    try:
        if form.validate_on_submit():
            url_AN =  clean_arg(request.form.get("url_AN", None))
            title =  clean_arg(request.form.get("title", None))
            name_authoress =  clean_arg(request.form.get("name_authoress", None))
            other_author =  clean_arg(request.form.get("other_author", None))
            name_theater =  clean_arg(request.form.get("name_theater", None))
            date =  clean_arg(request.form.get("date", None))
            type =  clean_arg(request.form.get("type", None))
            configuration =  clean_arg(request.form.get("configuration", None))
            is_published =  clean_arg(request.form.get("is_published", None))
            digitized =  clean_arg(request.form.get("digitized", None))

            # POUR LES CHAMPS OBLIGATOIRES
            # URL DE LA PIECE ET TITRE
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


            #  POUR L'AUTRICE
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
            
            #si le champs other_author est rempli
            if other_author:
                
                    other_author = Play(other_author=other_author)
                    db.session.add(other_author)
                    db.session.commit()
                
            

            if name_theater:
                theater_in_db = Theater.query.filter(Theater.id_theater == name_theater).all()
                
                if not theater_in_db:
                    new_theater = Theater(id_theater=name_theater)
                    db.session.add(new_theater)
                    db.session.commit()

            if date :
                new_date = Play(date=date)
                db.session.add(new_date)
                db.session.commit
            
            if configuration:
                configuration_in_db = Configuration.query.filter(Configuration.id_configuration == configuration).all()
                
                # s'il n'existe pas, on peut creer la nouvelle autrice
                if not configuration_in_db:
                    new_configuration = Configuration(id_configuration=configuration)
                    db.session.add(new_configuration)
                    db.session.commit()
                    print('Ca fonctionne')
                else:
                    print('Cette forme de pièce existe déjà.')
            
            if is_published:
                new_is_published = Play(is_published=is_published)
                db.session.add(new_is_published)
                db.session.commit()
            
            if digitized:
                new_digitized = Play(digitized=digitized)
                db.session.add(new_digitized)
                db.session.commit()
            flash("Les informations ont bien été inséré.")    
    except Exception as e :
        print(e)
        flash("Une erreur s'est produite lors de l'insertion des données:" + str(e), "error")
    return render_template("partials/formulaires/insertion_piece.html", 
            sous_titre= "Insertion piece" , 
            form=form)


# ROUTE INSERTION D'UNE AUTRICE
@app.route("/insertion/autrice", methods=['GET', 'POST'])
@login_required
def insertion_autrice():
    form = AddAuthoress()
    try:
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
        flash("Les informations ont bien été ajouté.")    
    except Exception as e :
        print(e)
        flash("Une erreur s'est produite lors de l'insertion des données:" + str(e), "error")
    return render_template("partials/formulaires/insertions.html", 
            sous_titre= "Insertion autrice" , 
            form=form)
