from flask import Flask, jsonify, request
from core.models import app, db
from core.models import Task, Note
from flask_migrate import Migrate
from sqlalchemy import exc
import core.logging_conf

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
        app.logger.info(f" Requested task with id {task_id} not found")
        return jsonify({'error': 'Task not found'}), 404


@app.route('/api/v1/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    
    task_name = data['name']
    task_desc = data['desc']
    
    try:
        new_task = Task(name=task_name, desc=task_desc)
        db.session.add(new_task)
        db.session.commit()
        app.logger.info({'msg': f'task with id {new_task.id} added successfully'})
        return jsonify({'msg': f'task with id {new_task.id} added successfully'})
    except exc.IntegrityError:
        db.session.rollback()
        app.logger.info({'msg': f'UNIQUE constraint failed, duplicate entry'})
        return jsonify({'msg': f'UNIQUE constraint failed, duplicate entry'})


@app.route('/api/v1/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):

    task = Task.query.get(task_id)
    
    if task:
        data = request.get_json()   
        if 'name' in data:
            task.name = data['name']
        if 'desc' in data:
            task.desc = data['desc']
        
        try:
            db.session.commit()
        except exc.IntegrityError:
            app.logger.error(f" Error update duplicate task with id {task_id}")
            return jsonify({'error': 'Duplicate  entry'}), 500

        app.logger.info({'msg': f'task with id {task_id} updated successfully'})
        return jsonify({'message': 'Task  updated'}), 200

    else:
        app.logger.info(f" Requested task with id {task_id} not found")
        return jsonify({'error': 'Task not found'}), 404

    
@app.route('/api/v1/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    
    if task:
        db.session.delete(task)
        db.session.commit()
        app.logger.info({'msg': f'task with {task_id} deleted successfully'})
        return jsonify({'msg': f'task with {task.id} deleted successfully'})
    else:
        app.logger.info({'error': f'Task with id {task_id} not found'})
        return jsonify({'error': 'Task not found'}), 404

