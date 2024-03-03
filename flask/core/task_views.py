from flask import Flask, jsonify, request
from core.models import app, db
from core.models import Task, Note
from flask_migrate import Migrate
from sqlalchemy import exc

migrate = Migrate(app, db)

@app.route('/api/v1/tasks', methods=['GET'])
def get_all_tasks():
    data = Task.query.all()
    tasks = [{'id': task.id, 'name': task.name, 'desc': task.desc} 
             for task in data]

    return jsonify({'Tasks': tasks})


@app.route('/api/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first()

    if task:
        task_data = {'id': task.id, 'task_name': task.name, 'task': task.desc}
        return jsonify({'task': task_data})
    else:
        return jsonify({'error': 'Task not found'}), 404


@app.route('/api/v1/add_task', methods=['POST'])
def add_task():
    data = request.get_json()
    
    task_name = data['name']
    task_desc = data['desc']
    
    try:
        new_task = Task(name=task_name, desc=task_desc)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'msg': f'note with id {new_task.id} added successfully'})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'msg': f'UNIQUE constraint failed, duplicate entry'})


@app.route('/api/v1/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):

    note = Task.query.get(task_id)

    if task:
        data = request.get_json()   
        if 'name' in data:
            task.name = data['name']
        if 'desc' in data:
            task.desc = data['desc']
        
        db.session.commit()
    
        return jsonify({'message': 'Task  updated'}), 200

    else:
        return jsonify({'error': 'Task not found'}), 404

    
@app.route('/api/v1/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'msg': f'user with {task.id} deleted successfully'})
    else:
        return jsonify({'error': 'Task not found'}), 404

