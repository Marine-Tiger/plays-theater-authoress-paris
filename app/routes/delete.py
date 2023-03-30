from ..app import app, db
from flask_login import login_required
from ..models.autrices import Play, Authoress, Theater

@app.route("/delete_autrice/<string:name>")
@login_required
def delete_autrices(name):
    
    Authoress.query.filter(Authoress.id == name).delete()
    db.session.commit()
    return('Succeeded')

@app.route("/delete_theatre/<string:name>")
@login_required
def delete_theatre(name):
    
    Theater.query.filter(Theater.id_play == name).delete()
    db.session.commit()
    return('Succeeded')

@app.route("/delete_piece/<string:name>")
@login_required
def delete_piece(name):
    
    Play.query.filter(Play.title == name).delete()
    db.session.commit()
    return('Succeeded')