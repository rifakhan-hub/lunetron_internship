# Create a Flask app runs on your local machine has a / route returns: welcome to my Flask 

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to my Flask"

# Create a GET /about endpoint that returns: This is my first Flask project
@app.route("/about", methods=["GET"])
def get_about():
    return "This is my first Flask project"

# Dynamic Route GET /hello/<name>
@app.route("/hello/<name>", methods=["GET"])
def hello(name):
    return f"Hello, {name}!"


if __name__ == "__main__":
    app.run(debug=True)
