from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

swagger = Swagger(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    department = db.Column(db.String(100))

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return "Flask CRUD API with SQLite Running"


@app.route('/students', methods=['GET'])
def get_students():
    

    students = Student.query.all()

    output = []

    for student in students:
        output.append({
            "id": student.id,
            "name": student.name,
            "department": student.department
        })

    return jsonify(output)


@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    

    student = Student.query.get(id)

    if not student:
        return jsonify({"message": "Student not found"}), 404

    return jsonify({
        "id": student.id,
        "name": student.name,
        "department": student.department
    })

@app.route('/students', methods=['POST'])
def add_student():
    

    data = request.json

    new_student = Student(
        name=data['name'],
        department=data['department']
    )

    db.session.add(new_student)
    db.session.commit()

    return jsonify({
        "message": "Student added successfully"
    }), 201


@app.route('/updatedata/<int:id>', methods=['PUT'])
def updateData(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"Message":"User not found"}),404
    data = request.json
    student.name = data.get('name', student.name)
    student.department = data.get('department', student.department)
    db.session.commit()
    return jsonify({"Message":"Data Updated"})


app.run(host='0.0.0.0', port=8090, debug=True)