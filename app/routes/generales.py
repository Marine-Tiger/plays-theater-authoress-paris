from ..app import app, db
from ..models.autrices import Play, Authoress
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os

# @app.route("/home", methods=["GET","POST"])
# def home():
#     plays = []
#     engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])
#     with engine.connect() as con:
#         rs = con.execute(text('SELECT * FROM play'))
#         for row in rs:
#             plays.append(str(row))
#     return plays
#     # for play in Play.query.all():
#     #     print(play.id_play)
#     # return "" 
@app.route("/home", methods=["GET","POST"])
def home():
    name = []
    for name_authoress in Authoress.query.all():
        name.append(name_authoress.id)
    return name
