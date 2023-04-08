from ..app import app, db
from flask import render_template
from ..models.autrices import Play, Type, play_type, Theater, play_theater, Configuration, play_configuration
from sqlalchemy import func, text

@app.route("/graphiques", methods=['GET', 'POST'])
def graphiques():
    return render_template("pages/graphiques.html")

@app.route("/graphiques/annees", methods=['GET', 'POST'])
def graphique_play_years():
     test_data= db.session.query(
          Play,\
          func.count(Play.date).label('total'),#COUNT(date) as total\ 
          # la func.substr() permet de conserver seulement l'année de la date, 
          # car elle est au format yyyy-MM-dd dans la base de données
          func.substr(Play.date, 0, 5).label('years')
          )\
     .filter(func.substr(Play.date, 0, 5))\
     .group_by(func.substr(Play.date, 0, 5))\
     # .order_by(text('total DESC'))

     data = []

     for year in test_data.all():
          print(year)
          data.append({
               # transformer le str en int permet de s'assurer que les résultats seront bien triés
               "label": int(year[2]),
               "nombre": year.total
          })

     print(data)

     return data

@app.route("/graphiques/genres", methods=['GET', 'POST'])
def graphique_type_play():
     test_data= db.session.query(Type, func.count(play_type.c.id_type).label('total'))\
     .join(play_type, )\
     .group_by(Type.id_type)\

     data = []

# Plutot que de limiter le nombre de résultats, on va créer un dictionnaire autres
     autres= {
          "label": 'Autres',
          "nombre": 0
     }

     for type in test_data.all():
          # Si le nombre total par genre est inférieur à 5
          if type.total < 5:
               # On ajoute à l'entrée 'nombre' le nombre total par genre
               autres['nombre'] += type.total
          else:
               data.append({
                    "label": type[0].id_type,
                    "nombre": type.total
               })
     # On ajoute le dictionnaire autres une fois la boucle terminée
     data.append(autres)
     return data

@app.route("/graphiques/theatre", methods=['GET', 'POST'])
def graphique_theater_play():
     raw_data= db.session.query(Theater, func.count(play_theater.c.id_theater).label('total'))\
    .join(play_theater, )\
     .group_by(Theater.id_theater)\

     data = []

     autres= {
          "label": 'Autres',
          "nombre": 0
     }
     
     for theater in raw_data.all():
          if theater.total < 4:
               autres['nombre'] += theater.total
          else:
               data.append({
                    "label": theater[0].id_theater,
                    "nombre": theater.total
               })
     data.append(autres)
     return data

@app.route("/graphiques/forme", methods=['GET', 'POST'])
def graphique_configuration_play():
     raw_data= db.session.query(Configuration, func.count(play_configuration.c.id_configuration).label('total'))\
    .join(play_configuration, )\
     .group_by(Configuration.id_configuration)\

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

     data = []

     for publication in raw_data.all():
          if publication[0].is_published == 1:
               data.append({
                    "label": 'Publiées',
                    "nombre": publication.total
               })
          else:
                    data.append({
                    "label": 'Non publiées',
                    "nombre": publication.total
               })

     return data