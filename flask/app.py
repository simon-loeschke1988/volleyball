from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://volley:volley@localhost/volley'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definieren Sie Ihre Modelle hier entsprechend den Django-Modellen

@app.route('/')
def index():
    return "Volleyball Web Application"

# Weitere Routen zur Verwaltung von Volleyballspielern, Matches und Turnieren

if __name__ == '__main__':
    app.run(debug=True)


app = flask.Flask(__name__)
app.config["DEBUG"] = True

