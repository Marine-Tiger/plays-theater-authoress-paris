from flask import url_for, render_template, redirect, request, flash
from flask_login import  login_user, current_user, logout_user
from ..models.users import Users
from ..models.formulaires import AjoutUtilisateur, Connexion
from ..utils.transformations import  clean_arg
from ..app import app, db, login


# ROUTE AJOUT UTILISATEUR
@app.route("/utilisateurs/ajout", methods=["GET", "POST"])
def ajout_utilisateur():
    form = AjoutUtilisateur()

    if form.validate_on_submit():
        statut, donnees = Users.ajout(
            prenom=clean_arg(request.form.get("prenom", None)),
            password=clean_arg(request.form.get("password", None))
        )
        if statut is True:
            flash("Ajout effectué", "success")
            return redirect(url_for("connexion"))
        else:
            flash(",".join(donnees), "error")
            return render_template("pages/ajout_utilisateur.html", form=form)
    else:
        return render_template("pages/ajout_utilisateur.html", form=form)
    
# ROUTE CONNEXION UTILISATEUR
@app.route("/utilisateurs/connexion", methods=["GET","POST"])
def connexion():
    form = Connexion()
    print(current_user)
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté", "info")
        return redirect(url_for("home"))

    if form.validate_on_submit():
        utilisateur = Users.identification(
            prenom=clean_arg(request.form.get("prenom", None)),
            password=clean_arg(request.form.get("password", None))
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect(url_for("home"))
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")
            return render_template("pages/connexion.html", form=form)

    else:
        return render_template("pages/connexion.html", form=form)

login.login_view = 'connexion'

# ROUTE DECONNEXION UTILISATEUR
@app.route("/utilisateurs/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté", "info")
    return redirect(url_for("home"))