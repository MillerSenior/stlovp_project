from flask import Flask

def create_app():
    """Flask application factory."""
    app = Flask(__name__)

    from app.routes import routes_bp  # Import blueprint
    app.register_blueprint(routes_bp)  # Register blueprint

    return app

app = create_app()
