import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    flask_kwargs = {}
    static_url_path = os.getenv("STATIC_URL_PATH")
    if static_url_path is not None:
        flask_kwargs["static_url_path"] = static_url_path

    app = Flask(__name__, **flask_kwargs)

    # Simple portal: only the index page with links to other systems.
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    if os.getenv("TRUST_PROXY", "").lower() in {"1", "true", "yes", "on"}:
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    from .routes.main import main_bp

    app.register_blueprint(main_bp)

    return app
