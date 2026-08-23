from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Create the Flask application
app = Flask(__name__)

# Telling Flask-SQLAlchemy which database to connect to :  mysql+pymysql://username:password@host/database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Mysql%402023@localhost/school"

# Create the SQLAlchemy object. This will be used to communicate between Flask and MySQL
db = SQLAlchemy()
db.init_app(app)        # Connect SQLAlchemy with our Flask application

class Student(db.Model):
    __tablename__ = "students"          # which existing MySQL table this model represents

    # defining columns of table

    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(50))
    age = db.Column(db.Integer)
    subject = db.Column(db.String(50))
    email= db.Column(db.String(50))

# application context so we can access the database
with app.app_context():
    db.create_all
    print("db connected")

@app.route("/students", methods=["GET"])
def get_students():

    students = Student.query.all()

    return jsonify([
        {
            "id" : student.id,
            "names": student.names,
            "subject": student.subject,
            "age": student.age,
            "email": student.email
        }
        for student in students
    ])

@app.route("/student/<int:id>", methods=["GET"])
def get_student(id):
    student = Student.query.get(id)

    if student:
        return jsonify(
            {
                "id" : student.id,
                "names": student.names,
                "subject": student.subject,
                "age": student.age, 
                "email": student.email
            }
        )

    return jsonify({"error": "student not found"}), 404

@app.route("/student", methods=["POST"])
def add_student():

    data = request.json

    student = Student(
        names = data["names"],
        age = data["age"],
        subject=data["subject"],
        email=data["email"]
    )

    db.session.add(student)
    db.session.commit()

    return jsonify ({
        "message": "student added successfully",
        "student": {
            "id": student.id,
            "names": student.names,
            "age": student.age,
            "subject": student.subject,
            "email": student.email
        }
    
    }), 201

if __name__=="__main__":
    app.run(debug=True)    