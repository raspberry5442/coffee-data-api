# app.py
from flask import Flask
from models import init_db
from routes import api

app = Flask(__name__)
app.register_blueprint(api)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
