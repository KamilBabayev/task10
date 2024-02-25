from flask import Flask, jsonify, request
from models import app, db
from models import Task, Note
from flask_migrate import Migrate

migrate = Migrate(app, db)

@app.route('/')
def index():
    return jsonify({"page": "index"})

@app.route('/api/v1/notes', methods=['GET'])
def get_all_notes():
    data = Note.query.all()
    notes = [{'id': note.id, 'username': note.name, 'email': note.note} 
             for note in data]

    return jsonify({'Notes': notes})

@app.route('/api/v1/notes/<int:id>', methods=['GET'])
def get_note_by_id():
    print("-----------")

    print(id)
    note = Note.query.filter_by(id=id).first()

    if note:
        note_data = {'id': note.id, 'note_name': note.name, 'note': note.note}
        return jsonify({'note': note_data})
    else:
        return jsonify({'error': 'Note not found'}), 404


@app.route('/api/v1/add_note', methods=['POST'])
def add_note():
    data = request.get_json()

    for k, v in data.items():
        note_name = k
        note = v

    new_note = Note(name=note_name, note=note)
    db.session.add(new_note)
    db.session.commit()
    return 'record successfully added'

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
