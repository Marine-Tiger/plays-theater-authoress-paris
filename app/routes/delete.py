from ..app import app, db
from flask import render_template, request
from ..models.autrices import Play, Authoress, Theater
from ..models.formulaires import PlayForm
from sqlalchemy import create_engine, exc
from sqlalchemy.sql import text
from sqlalchemy import or_
import os
from ..utils.transformations import  clean_arg

@app.route("/delete_autrice/<string:name>")
def delete_autrices(name):
    
    Authoress.query.filter(Authoress.id == name).delete()
    db.session.commit()
    return('Succeeded')

@app.route("/delete_theatre/<string:name>")
def delete_theatre(name):
    
    Theater.query.filter(Theater.id_play == name).delete()
    db.session.commit()
    return('Succeeded')

@app.route("/delete_piece/<string:name>")
def delete_piece(name):
    
    Play.query.filter(Play.title == name).delete()
    db.session.commit()
    return('Succeeded')