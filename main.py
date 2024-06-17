from flask import Flask
from thefs.api.api_v1 import api_v1


def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(api_v1)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
