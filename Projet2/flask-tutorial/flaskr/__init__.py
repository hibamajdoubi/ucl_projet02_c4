#contient l'usine à application
#flaskr doit être considéré comme un package

import os
from flask import Flask

"""
create_app est la fonction contenant l’usine à applications. Vous la compléterez plus tard dans ce tutoriel, mais elle réalise déjà beaucoup d’opérations.

app = Flask(__name__, instance_relative_config=True) crée une instance de la classe Flask.

__name__ est le nom du module Python courant. L’application doit connaître l’endroit où est elle installée pour configurer certains chemins et __name__ est une solution classique pour obtenir cette information.

instance_relative_config=True indique à l’application que les fichiers de configuration sont relatifs au répertoire instance folder. Ce répertoire est localisé en dehors du package flaskr et peut contenir des données locales qui ne doivent pas être intégrées au contrôle de version, comme les secrets utilisés dans la configuration et le fichier contenant la base de données.

app.config.from_mapping() spécifie plusieurs paramètres par défaut que l’application va utiliser:

SECRET_KEY est utilisé par Flask et des extensions pour stocker de données de façon sûre. Il est initialisé à la valeur 'dev' qui est une valeur facile pendant le développement de l’application, mais doit être remplacé par une valeur aléatoire lorsque celle-ci est mise en production.

DATABASE est le chemin où le fichier contenant la base de données SQLite sera sauvegardé. Le préfixe de ce fichier est app.instance_path, c’est-à-dire le chemin choisi par Flask comme instance folder. Vous en apprendrez plus sur la base de données dans la section suivante.

app.config.from_pyfile() remplace le configuration par défaut avec des paramètres spécifiés dans le fichier config.py qui se trouve dans l”instance folder si celui-ci exite. Par exemple, en production, cela peut être utilisé pour fixer une SECRET_KEY vraiment secrète.

La paramètre test_config peut aussi être passé à l’usine à applications. Dans ce cas, il sera utilisé à la place de la configuration de l’instance. Cela vous permettra de spécifier des paramètres pour vos test qui sont indépendants de ceux que vous utilisez durant le développement de l’application.

os.makedirs() vérifie que le chemin app.instance_path existe. Flask ne créer pas l’instance folder automatiquement, mais celui-ci doit être créé car votre projet cherhera à y créer le fichier contenant sa base de données SQLite.

@app.route() crée une route simple de façon à vous permettre de voir l’application fonctionner avant de faire l’entièreté du tutoriel. Elle relie l’URL /hello à une fonction qui retourne une réponse, dans ce cas la chaîne de caractères 'Hello, World!'.
"""


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
