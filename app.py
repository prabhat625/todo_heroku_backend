from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS

app= Flask(__name__)
CORS(app)

# different database for production and devlopment
ENV='PROD'
if ENV == 'PROD':
    app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://xkwjdpddhokzfg:8a678a487d63f4e0944d44177025f754d112ba7e305b0ef442356836df0fff0d@ec2-52-204-20-42.compute-1.amazonaws.com:5432/d4b9i9tq38h5b4'
else :
    app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:123456@localhost/todos_main'
    app.debug=True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)


class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    deleted=db.Column(db.Boolean,default=False)
    completed=db.Column(db.Boolean,default=False)

    #Return object data in serializable format
    def serialize(self):
        return { 
                'id': self.id,
                'name': self.name, 
                'deleted': self.deleted, 
                'completed': self.completed
                }


@app.route('/')
def index():
    return "Hello world"

# Api to check the connection
@app.route('/jsonrequest')
def jsonrequest():
    return jsonify({
        "success" : True
        })


# Api for listing all the present todos
@app.route('/todo/all',methods=['GET'])
def all_todos():
    all_todos=Todo.query.filter_by(deleted=False).order_by(Todo.id.asc()).all()
    list_all=[]
    for todo in all_todos:
        list_all.append(todo.serialize())
    return jsonify(list_all)

# Api for insertion of new todo 
@app.route('/todo/insert',methods=['POST'])
def insert():
    todo_json=request.get_json()
    if "name" not in todo_json:
        return jsonify({
            "success":False
        })
    name=todo_json['name']
    
    #if name not present or it is deleted then add 
    if Todo.query.filter_by(name=name).first() is None or \
        Todo.query.filter_by(name=name).first().deleted:
        todo_obj=Todo(name=name)
        db.session.add(todo_obj)
        db.session.commit()
        todo_ob_id=Todo.query.filter_by(name=name).first().id
        return jsonify({
            "success":True,
            "id":todo_ob_id
            })
    else : 
        return jsonify({
            "success":False
            })


#Api for completion or non-completion of task
@app.route('/todo/complete-or-not',methods=['POST'])
def mark_or_unmark_completed():
    obj_id=request.get_json()["id"]
    #holding the actual databse object
    todo_obj=Todo.query.filter_by(id=int(obj_id)).first()

    #if object with provided id exist in database then make change
    if todo_obj is not None:
        obj_completed=not todo_obj.completed
        if obj_completed :
            todo_obj.completed=True
        else :
            todo_obj.completed=False
        db.session.commit()
        return jsonify({
            "success":True
        })
    # if object dosn't exist in database
    else :
        return jsonify({
            "success":False
        })


#Api for soft delete of todo
@app.route('/todo/delete',methods=['POST'])
def delete_todo():
    todo_json=request.get_json()
    obj_id=todo_json.get("id")
    if obj_id is None :
         return jsonify({
            "success":False
        })
    #holding the actual databse object
    todo_obj=Todo.query.filter_by(id=int(obj_id)).first()

    #if object with provided id exist in database then soft delete it
    if todo_obj is not None:
        todo_obj.deleted=True
        db.session.commit()
        return jsonify({
            "success":True
        })
    # if object dosn't exist in database
    else :
        return jsonify({
            "success":False
        })


if __name__=='__main__':
    app.run()