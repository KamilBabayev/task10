from flask import Flask, jsonify, request
from core.models import app, db
from core.models import Task, Note
from flask_migrate import Migrate
from sqlalchemy import exc

import core.logging_conf

migrate = Migrate(app, db)

@app.route('/')
def index():
    return jsonify({"page": "index"})


@app.route('/api/v1/notes', methods=['GET'])
def get_all_notes():
    data = Note.query.all()
    notes = [{'id': note.id, 'name': note.name, 'desc': note.desc} 
             for note in data]

    return jsonify({'Notes': notes})


@app.route('/api/v1/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = Note.query.filter_by(id=note_id).first()

    if note:
        note_data = {'id': note.id, 'note_name': note.name, 'note': note.desc}
        return jsonify({'note': note_data})
    else:
        app.logger.info(f" Requested note with id {note_id} not found")
        return jsonify({'error': 'Note not found'}), 404


@app.route('/api/v1/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    
    note_name = data['name']
    note_desc = data['desc']
    
    new_note = Note(name=note_name, desc=note_desc)
    db.session.add(new_note)
    db.session.commit()

    app.logger.info({'msg': f'note with id {new_note.id} added successfully'})
    return jsonify({'msg': f'note with id {new_note.id} added successfully'})


@app.route('/api/v1/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):

    note = Note.query.get(note_id)

    if note:
        data = request.get_json()   
        if 'name' in data:
            note.name = data['name']
        if 'desc' in data:
            note.desc = data['desc']
        
        db.session.commit()

        app.logger.info({'msg': f'note with id {note_id} updated successfully'})
        return jsonify({'message': 'Note  updated'}), 200
    else:
        app.logger.info(f" Requested note with id {note_id} not found")
        return jsonify({'error': 'Note not found'}), 404

    
@app.route('/api/v1/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    
    if note:
        db.session.delete(note)
        db.session.commit()
        app.logger.info({'msg': f'note with {note_id} deleted successfully'})
        return jsonify({'msg': f'note with {note.id} deleted successfully'})
    else:
        app.logger.info({'error': f'Note with id {note_id} not found'})
        return jsonify({'error': 'Note not found'}), 404



