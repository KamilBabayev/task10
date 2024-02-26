from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///core.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(500), unique=True, nullable=False)
    status = db.Column(db.String(10))

    def __repr__(self):
        return f"Task('{self.id}', '{self.name}', '{self.desc}', '{self.status}')"
    
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    desc = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return f"Task('{self.id}', '{self.name}', '{self.desc}')"
