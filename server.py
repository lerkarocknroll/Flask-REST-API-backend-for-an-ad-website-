import os
from typing import Union
from flask import Flask, jsonify
from models import HTTPError  # вынесли HTTPError в models (см. ниже)
from routes import bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)

    @app.errorhandler(HTTPError)
    def handle_http_error(error):
        response = jsonify({'message': error.message})
        response.status_code = error.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
