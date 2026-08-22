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

# JSON Response GET /student
@app.route("/student/<id>", methods=["GET"])
def get_students(id):
    # data = {
    #     "id" : [1, 2, 3, 4],
    #     "name": ["A", "B", "C", "D"],
    #     "sub": ["math", "science", "math", "english"],
    #     "age": [10, 12, 11, 10]
    # }
    return jsonify(
        "students":[
    {
    "id": 1,
    "name": "Riya",
    "age": 21,
    "course": "AIML"
    }
    {
    "id": 2,
    "name": "Rahul",
    "age": 22,
    "course": "CSE"
    }
    {
    "id": 3,
    "name": "Ravi",
    "age": 20,
    "course": "AIML"
    }]
    )
    


if __name__ == "__main__":
    app.run(debug=True)
