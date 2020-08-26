from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy 

app= Flask(__name__)


ENV='DEV'
if ENV == 'PROD':
    app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://xkwjdpddhokzfg:8a678a487d63f4e0944d44177025f754d112ba7e305b0ef442356836df0fff0d@ec2-52-204-20-42.compute-1.amazonaws.com:5432/d4b9i9tq38h5b4'
else :
   app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:123456@localhost/todos_main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)


class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    deleted=db.Column(db.Boolean,default=False)
    completed=db.Column(db.Boolean,default=False)


@app.route('/')
def index():
    return "Hello world"

# Api to check the connection
@app.route('/jsonrequest')
def jsonreques():
    return jsonify([{"result" : "sucess"}])

# Api for insertion of new todo 
@app.route('/todo/insert',methods=['POST'])
def insert():
    todo_json=request.get_json()
    name=todo_json['name']
    
    #if name not present or it is deleted then add 
    if Todo.query.filter_by(name=name).first() is None or \
        Todo.query.filter_by(name=name).first().deleted:
        todo_obj=Todo(name=name)
        db.session.add(todo_obj)
        db.session.commit()
        return jsonify({"status":"success","completed":todo_obj.completed,"deleted":todo_obj.deleted})
    else :
        todo_obj=Todo.query.filter_by(name=name).first() 
        return jsonify({"status":"already_exists","completed":todo_obj.completed,"deleted":todo_obj.deleted})

if __name__=='__main__':
    app.debug=True
    app.run()