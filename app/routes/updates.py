from ..app import app, db
from flask import render_template, request, flash
from flask_login import login_required
from ..models.autrices import Play, Authoress, Theater
from ..models.formulaires import Update
from sqlalchemy.sql import text
from sqlalchemy import or_
import os
from ..utils.transformations import  clean_arg

@app.route("/update/autrice/<string:name>", methods=['GET', 'POST'])
@login_required
def update_autrice(name):
    form = Update()
    try:
        if form.validate_on_submit():
            name_authoress =  clean_arg(request.form.get("name_authoress", None))
            lien_wikipedia = clean_arg(request.form.get("lien_wikipedia", None))
            id_wikidata = clean_arg(request.form.get("lien_wikipedia", None))
            lien_bnf = clean_arg(request.form.get("lien_wikipedia", None))

            update = {}
            if name_authoress:
                update['id'] = name_authoress
            
            if lien_wikipedia:
                update['wikipedia'] = lien_wikipedia

            if id_wikidata:
                update['wikidata'] = id_wikidata

            if lien_bnf:
                update['bnf'] = lien_bnf

            Authoress.query.filter(Authoress.id == name).update(update)                
            db.session.commit()

        flash("Les informations ont bien été mises à jour.")    
    except Exception as e :
        print(e)
        flash("Une erreur s'est produite lors de la mise à jour des données:" + str(e), "error")
    
    return render_template("partials/formulaires/update_autrice.html", 
            sous_titre= "Update autrice", 
            name=name,
            form=form)

@app.route("/update/play/<string:id_play>", methods=['GET', 'POST'])
@login_required
def update_play(id_play):
    form = Update()
    try:
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
        flash("Les informations ont bien été mises à jour.")    
    except Exception as e :
        print(e)
        flash("Une erreur s'est produite lors de la mise à jour des données:" + str(e), "error")
  

    return render_template("partials/formulaires/update_play.html", 
            sous_titre= "Update piece" , 
            id_play=id_play,
            form=form)
        
        

