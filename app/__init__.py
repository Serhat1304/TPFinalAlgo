from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importer et enregistrer les blueprints
    from app.routes import bp
    app.register_blueprint(bp)

    return app
