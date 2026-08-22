from flask import Flask, jsonify, request

app = Flask(__name__)

students = [
    {
        "id": 1,
        "name": "Riya",
        "age": 21,
        "course": "AIML"
    },
    {
        "id": 2,
        "name": "Rahul",
        "age": 22,
        "course": "CSE"
    }
]

@app.route("/student", methods=["POST"])
def add_student():
    data = request.json

    students.append(data)

    return jsonify(students)

if(__name__) == "__main__":
    app.run(debug=True)
