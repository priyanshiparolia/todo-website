from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#config key from sqlalchemy website
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
with app.app_context():
    db = SQLAlchemy(app)

 #helps python to connect with database

 #database class
class Todo(db.Model):
    #fields
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
#when obj of this class will be made whatever we want to see will be sent from repr
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}" #we want to see its serial number and title

#when someone will come to homepage an instance of todo will be created
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title'] #datafrom the form will be stored in title
        desc = request.form['desc'] #getting the data
        todo = Todo(title=title, desc=desc) #instance
        db.session.add(todo) 
        db.session.commit() #changes will be commited
        
    allTodo = Todo.query.all() 
    return render_template('index.html', allTodo=allTodo) #sending alltodo in index.html with the help of jinja2

@app.route('/show') #showing all the todos, it execute repr func
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/") #redirect to first page 

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')