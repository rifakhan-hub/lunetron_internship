from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


with app.app_context():
    db.create_all()

@app.route("/students", methods=["POST"])
def create_student():

    data = request.get_json()

    student = Student(
        name=data["name"],
        email=data["email"],
        course=data["course"]
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student created successfully",
        "id": student.id
    }), 201


@app.route("/")
def home():
    return "Flask Database is Working"


if __name__ == "__main__":
    app.run(debug=True)