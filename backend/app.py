from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app= Flask(__name__)
db=SQLAlchemy(app)

ENV='DEV'
if ENV == 'PROD':
    app.config['SQLALCHEMY_DATABASE_URI']='postgres://xkwjdpddhokzfg:8a678a487d63f4e0944d44177025f754d112ba7e305b0ef442356836df0fff0d@ec2-52-204-20-42.compute-1.amazonaws.com:5432/d4b9i9tq38h5b4'
else :
   app.config.update({'SQLALCHEMY_DATABASE_URI':'postgres://postgres:123456@localhost/todo_db'})
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    deleted=db.Column(db.Boolean,default=False)
    completed=db.Column(db.Boolean,default=False)

@app.route('/')
def index():
    return "Hello world"

if __name__=='__main__':
    app.debug=True
    app.run()