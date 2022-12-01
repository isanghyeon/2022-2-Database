from flask import (
    Flask, g
)
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
import sys, os, json, datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.modelObj import shop


def create_app(config=None):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    CORS(app, resource={r'/api/*': {"Access-Control-Allow-Origin": "*"}})
    CORS(app, resource={r'/api/*': {"Access-Control-Allow-Credentials": True}})

    # Config initialization
    from config import Developments_config, Production_config
    app.config['DEBUG'] = False  # NOT TESTING is False or TESTING is True
    if app.config['DEBUG']:
        config = Developments_config()
    else:
        config = Production_config()

    app.config.from_object(config)

    # Register routing for blueprint
    from controller import bp as api
    app.register_blueprint(api)

    # App context initialization
    app.app_context().push()

    # DB initialize and migrate
    shop.init_app(app)
    shop.app = app

    if app.config['DEBUG']:
        # Database create
        from models.shop.cart import cart
        from models.shop.consumer import consumer
        from models.shop.product import product
        from models.shop.producer import producer

        # shop.create_all()

    @app.before_request
    def before_request():
        g.dbSession = shop.session()

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'dbSession'):
            g.dbSession.close()

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host="localhost", port=5000, debug=True)
