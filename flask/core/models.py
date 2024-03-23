from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///core.db'
db = SQLAlchemy(app)

def custom_default_date():
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    date_object = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    return date_object

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(500), unique=True, nullable=False)
    status = db.Column(db.Enum('open', 'in_progress', 'done'), default='open')
    created_at = db.Column(db.DateTime, default=custom_default_date)

    def __repr__(self):
        return f"Task('{self.id}', '{self.name}', '{self.desc}', \
                      '{self.created_at}', {self.status}')"
    
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    desc = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return f"Task('{self.id}', '{self.name}', '{self.desc}')"
