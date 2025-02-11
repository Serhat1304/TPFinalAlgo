from flask import Flask

from setup_db import create_connection, create_table


def create_app():
    app = Flask(__name__)

    # Importer et enregistrer les blueprints
    from app.routes import bp
    app.register_blueprint(bp)
    connection = create_connection()

    create_table(connection)

    return app
