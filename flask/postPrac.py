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
    data["id"] = len(students) + 1      # when there is no id 
    students.append(data)

    return jsonify(students)


# PUT request to update the data
@app.route("/student/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.json
    for student in students:
        if student["id"] == id:
            student["name"] = data["name"]
            student["age"] = data["age"]
            student["course"] = data["course"]
            return jsonify(student)

    return jsonify({"error": "invalid id"}), 404



if(__name__) == "__main__":
    app.run(debug=True)
