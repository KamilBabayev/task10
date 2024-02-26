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
    print(data)
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
        return jsonify({'error': 'Note not found'}), 404


@app.route('/api/v1/add_note', methods=['POST'])
def add_note():
    data = request.get_json()

    for k, v in data.items():
        note_name = k
        note_desc = v

    new_note = Note(name=note_name, desc=note_desc)
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'msg': f'user with {new_note.id} added successfully'})


@app.route('/api/v1/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):

    note = Note.query.get(note_id)
    # note = Note.query.filter_by(id=note_id).first()
    print(note_id)
    print(note)

    if note:
        data = request.get_json()   
        print(data)
        if 'name' in data:
            note.name = data['name']
        if 'desc' in data:
            note.desc = data['desc']
        
        db.session.commit()

        # if ''
        # for k, v in data.items():
        #     updated_note_name = k
        #     updated_note_desc = v    
        # print(data)
        # print(updated_note_desc, updated_note_name)
    
        return jsonify({'message': 'Note  updated'}), 200

    else:
        return jsonify({'error': 'Note not found'}), 404

    
@app.route('/api/v1/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'msg': f'user with {note.id} deleted successfully'})
    else:
        return jsonify({'error': 'Note not found'}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
