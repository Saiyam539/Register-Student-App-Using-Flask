from flask import Flask,render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class student(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    classes = db.Column(db.String(10), nullable=False)
    roll_no = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"{self.number}- {self.name}, {self.classes}, {self.roll_no}"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form' , methods=['GET','POST'])
def forms():
    if request.method == 'POST':
        number = request.form['number']
        name = request.form['name']
        classes = request.form['class']
        roll_no = request.form['roll_no']
        students = student(number=number, name=name, classes=classes, roll_no=roll_no)
        db.session.add(students)
        db.session.commit()
        return redirect('/') 

    return render_template('form.html',student=student.query.all())

@app.route('/list', methods=['GET','POST'])
def list():
    global number, name, classes, roll_no
    all_students = student.query.all()
    return render_template('list.html', student=all_students)


@app.route('/details/<int:sno>', methods=['GET','POST'])
def details(sno):
    global number, name, classes, roll_no
    info = student.query.filter_by(sno=sno).first()
    return render_template('details.html', student=info)

@app.route('/delete/<int:sno>', methods=['GET','POST'])
def delete(sno):
    global number, name, classes, roll_no
    info = student.query.filter_by(sno=sno).first()
    db.session.delete(info)
    db.session.commit()
    return redirect('/list')

if __name__ == '__main__':
    app.run(debug=True)