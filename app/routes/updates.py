from ..app import app, db
from flask import render_template, request
from ..models.autrices import Play, Authoress, Theater
from ..models.formulaires import Update
from sqlalchemy.sql import text
from sqlalchemy import or_
import os
from ..utils.transformations import  clean_arg

@app.route("/update/autrices", methods=['GET', 'POST'])
def update_authoress_name():
    form = Update()

    if form.validate_on_submit():
        name_authoress =  clean_arg(request.form.get("name_authoress", None))
        new_name_authoress =  clean_arg(request.form.get("new_name_authoress", None))

        update = {}
        if name_authoress:
            authoress_in_db = Authoress.query.filter(Authoress.id == name_authoress).all()
            if authoress_in_db is not None:
                Authoress.query.filter(Authoress.id == name_authoress).update({"id": new_name_authoress})

                db.session.commit()
                print('Ca fonctionne')
            else:
                print('Cette autrice existe déjà.')
            db.session.commit()
    
    return render_template("partials/formulaires/update_autrice.html", 
            sous_titre= "Update autrices" , 
            form=form)

@app.route("/update/play/<string:id_play>", methods=['GET', 'POST'])
def update_play(id_play):
    form = Update()

    if form.validate_on_submit():
        new_url_AN =  clean_arg(request.form.get("url_AN", None))
        new_title_play=  clean_arg(request.form.get("title_play", None))
        new_date =  clean_arg(request.form.get("date", None))
        new_is_published =  clean_arg(request.form.get("new_is_published", None))
        new_digitized =  clean_arg(request.form.get("new_digitized", None))
        new_other_author =  clean_arg(request.form.get("new_other_author", None))
        
        # On crée un dictionnaire pour stocker les updates à chaque champs du formulaire rempli
        update = {}
    
        if new_url_AN:
            update['url_AN'] = new_url_AN

        if new_title_play:
            update['title'] = new_title_play

        if new_date:
            update['date'] = new_date

        if new_is_published:
            update['is_published'] = new_is_published

        if new_digitized:
            update['digitized'] = new_digitized


        if new_other_author:
            update['other_author'] = new_other_author
    

        Play.query.filter(Play.id_play == id_play).update(update)                
        db.session.commit()
  

    return render_template("partials/formulaires/update_play.html", 
            sous_titre= "Update piece" , 
            id_play=id_play,
            form=form)
        
        

