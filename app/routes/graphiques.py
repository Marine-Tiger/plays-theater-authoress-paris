from ..app import app, db
from flask import render_template, request, flash
from flask_login import login_required
from ..models.autrices import Play, Type, play_type
from sqlalchemy import func, text

@app.route("/graphiques", methods=['GET', 'POST'])
def graphiques_ressources_pays():
    return render_template("pages/graphiques.html")

@app.route("/graphiques/test", methods=['GET', 'POST'])
def graphiques_type_play():
     test_data= db.session.query(Type, func.count(play_type.c.id_type).label('total'))\
    .join(play_type, )\
     .group_by(Type.id_type)\
     .order_by(text('total DESC'))\
     .limit(20)

     data = []

     for type in test_data.all():
          data.append({
               "label": type[0].id_type,
               "nombre": type.total
          })

     return data