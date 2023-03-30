from ..app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prenom = db.Column(db.Text(500), nullable=False)
    password = db.Column(db.Text(500), nullable=False)

    @staticmethod
    def ajout(prenom, password):
        erreurs = []
        if not prenom:
            erreurs.append("Le prénom est vide")
        if not password or len(password) < 6:
            erreurs.append("Le mot de passe est vide ou trop court")

        unique = Users.query.filter(
            db.or_(Users.prenom == prenom)
        ).count()
        if unique > 0:
            erreurs.append("Le prénom existe déjà")

        if len(erreurs) > 0:
            return False, erreurs
        
        utilisateur = Users(
            prenom=prenom,
            # pour ne pas stocker le mot de passe en clair
            password=generate_password_hash(password)
        )

        try:
            db.session.add(utilisateur)
            db.session.commit()
            return True, utilisateur
        except Exception as erreur:
            db.session.rollback()
            return False, [str(erreur)]
        
    def get_id(self):
        return self.id
    
    @login.user_loader
    def get_user_by_id(id):
        return Users.query.get(int(id))
    
    @staticmethod
    def identification(prenom, password):
        utilisateur = Users.query.filter(Users.prenom == prenom).first()
        if utilisateur and check_password_hash(utilisateur.password, password):
            return utilisateur
        return None
