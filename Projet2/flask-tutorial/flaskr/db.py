import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

"""
g est un objet spécial qui est unique pour chaque requête. Il est utilisé pour stocker des données qui pourraient être accédées par plusieurs fonctions durant le traitement de la requête. La connexion est conservée et réutilisée si get_db est appelé une deuxième fois dans le traitement de la même requête.

current_app est un autre objet spécial qui pointe vers l’application Flask qui traite la requête. Comme vous avez utilisé une usine à application, il n’y a pas d’objet application en écrivant la suite de votre code. get_db sera appelée lorsque l’application a été créée et qu’elle traite une requête. De cette façon, current_app peut être utilisé.

sqlite3.connect() crée une connexion avec le fichier correspondant au paramètre de configuration DATABASE. Il n’est pas nécessaire que ce fichier existe. Il sera créé plus tard lors de l’initialisation de la base de données.

Le paramètre sqlite3.Row indique que la connexion doit retourner des lignes qui sont équivalentes à des dictionnaires Python. Cela permet d’accéder aux colonnes en indiquant leur nom.

close_db vérifie si une connexion a été créée en regardant si g.db a été initialisé. Si la connexion existe, elle est fermé. Vous apprendrez plus tard à votre application d’utiliser la fonction close_db depuis l’usine à applications de façon à l’appeler automatiquement après le traitement de chaque requête.
"""


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


"""
open_resource() ouvre un fichier qui est relatif au package flaskr. L’utilisation d’un chemin relatif est intéressant car vous ne saurez pas nécessairement quel sera ce répertoire lorsque vous mettrez votre application en production. get_db retourne une connection à la base de données, qui est utilisée pour exécuter les commandes lues dans le fichier passé en argument.

click.command() définit uns interface en ligne de commande baptisée init-db qui appelle la fonction init_db and affiche un message de réussite à l’utilisateur. Vous pouvez lire le document :ref:`cli`pour en savoir plus sur comment écrire de telles commandes.
"""

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext

def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
