import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)

  return app

app = create_app()

@app.route('/')
def test():
  return "Hello!"

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)