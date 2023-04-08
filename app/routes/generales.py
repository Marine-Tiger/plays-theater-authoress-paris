from ..app import app, db
from flask import render_template
from ..models.autrices import Play, Authoress, Theater, Quote
# librairie pour importer des informations de wikipedia
import wikipedia
import urllib
# librairie pour effectuer des requetes SPARQL dans Wikidata
from SPARQLWrapper import SPARQLWrapper, JSON


@app.route("/home")
def home():
    return render_template('pages/home.html')

# PAGE LISTE DES AUTRICES
@app.route("/autrices")
@app.route("/autrices/<int:page>")
def autrices(page=1):
    return render_template ('pages/liste_autrices.html',
                            sous_titre = 'Index des autrices',
                            donnees=Authoress.query.order_by(Authoress.id).paginate(page=page, per_page=app.config["AUTRICES_PER_PAGE"]))


# PAGE DE PRESENTATION DES AUTRICES
@app.route("/autrices/<string:name>")
def presentation(name):
    data= db.session.query(Authoress, Play)\
    .join(Play.Authoress).\
    filter(Authoress.id == name).all()
    authoress = {}

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


    # Python ne sait pas comment transformer une instance de classe en json car impossible 
    # (une instance de classe peut contenir des fonctions/attributs prives/publics = pas representable en json)
    # ==> on transf la donnee en dict que python sait serialiser (transfo) en json (donc en donnees les unes a la suite des autres)

    # creation d'une variable autrice qui stocke l'elmt[0] la tuple
    autrice=data[0][0]
    # on ajoute au dictionnaire une clef dont la valeur est le 1er elmt de la tuple
    # pour transformer l'elmt en dictionnaire, on accede a sa propriete via le .[propriete] ==> propriete qui est un string ici
    authoress['authoress'] = {
        'id': autrice.id, 
        'wikipedia': autrice.wikipedia, 
        'wikidata': autrice.wikidata,
        'bnf': autrice.bnf,
        'img_wiki': autrice.url_image_wikipedia
    }

    # Pour ajouter les proprietes de la classe Play
    # La clef 'piece' a pour valeur une liste
    authoress['piece'] =  [
    ]
    
    # Pour recuperer les donnees de la table Play
    for elm in data:
        # une variable piece qui vaut la position une dans la tuple
        piece=elm[1]
        # a chaque tour, on ajoute a la liste les differents elements de la table Play
        authoress['piece'].append({'cote_AN':piece.url_AN, 
                                      'titre':piece.title, 
                                      'date': piece.date, 
                                      'autre auteur': piece.other_author, 
                                      'lien numerisation':piece.digitized,
                                      'publié': piece.is_published == 1})
    
    # REQUETE SPARQL POUR RECUPERER UNE IMAGE DANS WIKIDATA
    if authoress['authoress']['wikidata'] is not None and authoress['authoress']['img_wiki'] is None:

        # stockage dans une variable de l'url wikidata
        wikidata_url= authoress['authoress']['wikidata']

        # split pour recuperer seulement l'entite ID wikidata
        wikidata_entity = wikidata_url.split('/')
        wikidata_entity_id = wikidata_entity[-1]
        # La requete SPARQL, on ajoute la variable wikidata_entity_id grace au + (concatenation)
        sparql_query = """
            SELECT ?pic
            WHERE
            {
            ?item wdt:P18 ?pic .
            FILTER(?item = wd:""" + wikidata_entity_id + """)
            SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
            }
            LIMIT 1
            """
        # Envoie la requete à exécuter à la librairie
        sparql.setQuery(sparql_query)
        # On récupère le format en JSON = dictionnaire
        sparql.setReturnFormat(JSON)
        # Converti avec tous les paramètres donnés
        sparql_res = sparql.query().convert()
        
        # pour être sûr de récupérer celles qui ont des images
        try:
            result = sparql_res['results']['bindings'][0]['pic']['value']
            # on ajoute le résultat à la table Authoress
            Authoress.query.filter(Authoress.id == name).update({'url_image_wikipedia': result})
            # on ajoute au dicitonnaire authoress
            authoress['authoress']['img_wiki'] = result
        except Exception as e:
            print(e)

    # POUR RECUPERER UN RESUME DE WIKIPEDIA
    if authoress['authoress']['wikipedia'] is not None:
        wikipedia.set_lang("fr")
        name = authoress['authoress']['wikipedia']
        name_split= name.split('/')
        name_parse = urllib.parse.unquote(name_split[-1])
        wiki_page = wikipedia.page(name_parse, auto_suggest=False)
        authoress['authoress']['summary'] = wiki_page.summary

    return render_template ('pages/presentation_autrice.html',
                            authoress=authoress,
                            name=name)


# PAGE DES PIECES DE THEATRE
@app.route("/pieces")
@app.route("/pieces/<int:page>")
def pieces(page=1):
     return render_template('pages/liste_pieces.html',
                            sous_titre = 'Index des pièces de théâtre',
                            donnees=Play.query.order_by(Play.title).paginate(page=page, per_page=app.config["PIECES_PER_PAGE"]))



# PAGE POUR CHAQUE PIECE
@app.route("/pieces/<string:titre>")
def presentation_piece(titre):
    # J'effectue une requete SQLAlchemy pour recuperer les informations des tables Play, Configuration, Theater et Type 
    # en faisant un .join avec les jointures declarees dans la class Play
    data= db.session.query(Play)\
    .select_from(Play)\
    .join(Play.configuration)\
    .join(Play.theater)\
    .join(Play.type)\
    .filter(Play.title == titre).one()
    # Je renvoie vers la template
    return render_template ('pages/presentation_piece.html',
                            # pour pouvoir utiliser les resultats contenus dans data qui est une liste, 
                            # je cree une variable piece qui va contenir la liste de l'ensemble des informations requêtées
                            # même si je sais qu'il n'y a qu'une seule piece, je suis obligee de le preciser avec le [0] 
                            # car la machine ne le sait pas
                            piece = data,
                            titre = titre)


# PAGE POUR LES THEATRES
@app.route("/theatres")
@app.route("/theatres/<int:page>")
def theatres(page=1):
     return render_template('pages/liste_theatre.html',
                            sous_titre = 'Index des théâtres',
                            donnees=Theater.query.order_by(Theater.id_theater).paginate(page=page, per_page=app.config["THEATRES_PER_PAGE"]))

@app.route("/theatres/<string:theatre>")
def theatre_piece(theatre):
    data= db.session.query(Theater, Play)\
    .join(Play.theater)\
    .filter(Theater.id_theater == theatre).all()

    print(data)

    theatre_pieces = data[0][0]

    liste_pieces_theatre={}
    liste_pieces_theatre['theatre']={
        'id_theater': theatre_pieces.id_theater
    }

    liste_pieces_theatre['liste_pieces']=[

    ]

    for elm in data:
        pieces = elm[1]
        liste_pieces_theatre['liste_pieces'].append({
                    'titre': pieces.title
        })

    return render_template('pages/liste_theatre_pieces.html',
                        data = data,
                        liste_pieces_theatre=liste_pieces_theatre)


    
