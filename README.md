# Les autrices dans le théâtre #

Cette application a pour objectif de faire connaître les dramaturges produites dans les salles parisiennes du début du 19ème siècle au début du 20ème siècle.

Réalisée dans le cadre  de la deuxième année de Master Technologies Numériques Appliquées à l'Histoire à l'Ecole Nationale des Chartes, cette API exploite une base de donnée créée à partir des données fournies par le site _[data.gouv](https://www.data.gouv.fr/fr/datasets/pieces-de-theatre-ecrites-par-des-femmes-et-representees-a-paris-entre-1809-et-1906/)_.

Elle permet de découvrir ces autrices et leurs pièces, mais aussi de participer à l'enrichissement de la base de données en ajoutant ou modifiant les informations concernant les dramaturges et/ou leurs oeuvres.

## Installations ##

Ce repository contient la base de données en .sqlite, il n'est donc pas nécessaire de la télécharger. 
Pour installer l'application:

- Récupérer le dépôt: 
```git clone https://github.com/Marine-Tiger/plays-theater-authoress-paris```

- Récupérer les modules nécessaires pour faire fonctionner l'application:
```pip install -r requirements.txt```

- Créer un .env à la racine de l'application et y coller les lignes suivantes:
```DEBUG=True
SQLALCHEMY_DATABASE_URI=sqlite:///chemin vers la base de données

WTF_CSRF_ENABLE=True
SECRET_KEY=tnah2023

AUTRICES_PER_PAGE=20
PIECES_PER_PAGE=20
THEATRES_PER_PAGE=20
```
