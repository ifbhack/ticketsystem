import os
from flask import Flask

def create_app(test_config=None):
    """create and configure the ticket system"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, "ticket.db"),
    )

    from . import db
    db.prepare_app_callbacks(app)

    from . import ticket
    app.register_blueprint(ticket.bp)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
