from ..app import app, db
from flask import render_template, request, flash
from flask_login import login_required
from ..models.autrices import Play, Type, play_type, Theater, play_theater, Configuration, play_configuration
from sqlalchemy import func, text

@app.route("/graphiques", methods=['GET', 'POST'])
def graphiques_ressources_pays():
    return render_template("pages/graphiques.html")

@app.route("/graphiques/genres", methods=['GET', 'POST'])
def graphique_type_play():
     test_data= db.session.query(Type, func.count(play_type.c.id_type).label('total'))\
    .join(play_type, )\
     .group_by(Type.id_type)\
     .order_by(text('total DESC'))\
     .limit(10)

     data = []

     for type in test_data.all():
          data.append({
               "label": type[0].id_type,
               "nombre": type.total
          })

     return data

@app.route("/graphiques/theatre", methods=['GET', 'POST'])
def graphique_theater_play():
     raw_data= db.session.query(Theater, func.count(play_theater.c.id_theater).label('total'))\
    .join(play_theater, )\
     .group_by(Theater.id_theater)\
     .order_by(text('total DESC'))\
     .limit(10)


     data = []

     for theater in raw_data.all():
          data.append({
               "label": theater[0].id_theater,
               "nombre": theater.total
          })

     return data

@app.route("/graphiques/forme", methods=['GET', 'POST'])
def graphique_configuration_play():
     raw_data= db.session.query(Configuration, func.count(play_configuration.c.id_configuration).label('total'))\
    .join(play_configuration, )\
     .group_by(Configuration.id_configuration)\
     .order_by(text('total DESC'))

     data = []

     for configuration in raw_data.all():
          data.append({
               "label": configuration[0].id_configuration,
               "nombre": configuration.total
          })

     return data


@app.route("/graphiques/publication", methods=['GET', 'POST'])
def graphique_is_published():
     raw_data= db.session.query(Play, func.count(Play.is_published).label('total'))\
     .group_by(Play.is_published)\
     .order_by(text('total DESC'))

     data = []

     for publication in raw_data.all():
          data.append({
               "label": publication[0].is_published,
               "nombre": publication.total
          })

     return data