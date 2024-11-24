from flask import Flask, jsonify, request
from core.models import app, db
from core.models import Task, Note
from flask_migrate import Migrate
import core.task_views
import core.note_views
import core.logging_conf

migrate = Migrate(app, db)

@app.errorhandler(404)
def not_found(error):
    app.logger.info({"message": "route not found"})
    return jsonify({"message": "route not found"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
