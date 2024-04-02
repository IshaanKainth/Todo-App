from flask import Flask,render_template,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__,template_folder='template')
engine = create_engine("root:IshaanKainth-1234@localhost:3306/todo", pool_size=10, max_overflow=20)
app.config['SQLALCHEMY_DATABASE_URI']=engine
# 'mysql+pymysql://root:IshaanKainth-1234@localhost:3306/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=True)
    description=db.Column(db.String(500), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f'<Todo {self.title} , {self.description}>'  

with app.app_context():
    db.create_all()

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        todo=Todo(title=title,description=description)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template('index.html',alltodo=alltodo)


@app.route('/edit/<int:id>')
def edit(id):
    todo = Todo.query.get(id)
    return render_template('update.html',atodo=todo)

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
        if request.method=='POST':
            atodo = Todo.query.get(id)
            title=request.form['title']
            description=request.form['description']
            atodo.title = title
            atodo.description = description
            atodo.date_created = datetime.utcnow()
            db.session.commit()
        return redirect("/")

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")




# if __name__=="__main__":
#     app.run(debug=True)

