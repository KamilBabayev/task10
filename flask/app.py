from flask import Flask, jsonify, request
from core.models import app, db
from core.models import Task, Note
from flask_migrate import Migrate
import core.task_views
import core.note_views

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
