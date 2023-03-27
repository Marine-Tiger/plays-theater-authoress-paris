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

        authoress_in_db = Authoress.query.filter(Authoress.id == name_authoress).all()
        if authoress_in_db is not None:
            Authoress.query.filter(Authoress.id == name_authoress).update({"id": new_name_authoress})

            db.session.commit()
            print('Ca fonctionne')
        else:
            print('Cette autrice existe déjà.')
        db.session.commit()
    
    return render_template("partials/update_autrice.html", 
            sous_titre= "Update autrices" , 
            form=form)

@app.route("/update/play", methods=['GET', 'POST'])
def update_play():
    form = Update()

    if form.validate_on_submit():
        name_authoress =  clean_arg(request.form.get("name_authoress", None))
        new_name_authoress =  clean_arg(request.form.get("new_name_authoress", None))
        url_AN =  clean_arg(request.form.get("url_AN", None))
        new_url_AN =  clean_arg(request.form.get("new_url_AN", None))
        title_play=  clean_arg(request.form.get("new_name_authoress", None))
        new_title_play=  clean_arg(request.form.get("new_name_authoress", None))
        date =  clean_arg(request.form.get("name_authoress", None))
        new_date =  clean_arg(request.form.get("name_authoress", None))
        is_published =  clean_arg(request.form.get("new_name_authoress", None))
        new_is_published =  clean_arg(request.form.get("new_name_authoress", None))
        digitized =  clean_arg(request.form.get("name_authoress", None))
        new_digitized =  clean_arg(request.form.get("name_authoress", None))
        other_author =  clean_arg(request.form.get("new_name_authoress", None))
        new_other_author =  clean_arg(request.form.get("new_name_authoress", None))

    
    
    # if url_AN or title_play or date or is_published or digitized or other_author:
    #     # Play.query.\
    #     #     filter(Play.id_play == url_AN, Play.title == title_play, Play.date == date, Play,is_published == is_published, Play.digitized == digitized, Play.other_author == other_author).update({Play.id_play == new_url_AN, Play.title == new_title_play, Play.date == new_date, Play,is_published == new_is_published, Play.digitized == new_digitized, Play.other_author == new_other_author})
        
    #     db.session.update()
    #     db.session.commit()
        
    # return render_template("partials/update_autrice.html", 
    #         sous_titre= "Update autrices" , 
    #         form=form)
        
        

# def update_autrices(current_name, new_name):
    
#     Authoress.query.filter(Authoress.id == current_name).update({"id": new_name})
#     db.session.commit()
#     return "Succeded"

# @app.route("/update_theatre/<string:current_name>/<string:new_name>")
# def update_theatre(current_name, new_name):

#     Theater.query.filter(Theater.id_theater== current_name).update({"id_theater": new_name})
#     db.session.commit()
#     return "Succeded"

# @app.route("/update_piece/<string:current_name>/<string:new_name>")
# def update_piece(current_name, new_name):

#     Play.query.filter(Play.title== current_name).update({"title": new_name})
#     db.session.commit()
#     return "Succeded"