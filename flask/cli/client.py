import requests
import click
from tabulate import tabulate
from datetime import datetime

api_url = 'http://localhost:5000/api/v1/'

@click.group()
def cli():
    pass

@click.group('task', help='Task management')
def task():
    print()

@click.group('note', help='Note management')
def note():
    print()

@task.command('get', help='get task details')
@click.option('--id', help='specify task id to get')
@click.option('--all', is_flag=True, help='get all tasks')
def get(id, all):
    if id is None and all is False:
        print("enter --id <id> to get specific task or --all to get all tasks")
    elif id is None and all is True:
        req = requests.get(api_url + "tasks")

        if len(req.json()['Tasks']) == 0:
            print(req.json())
            return
        
        print("got all tasks for you")
        tasks = []
        for task in req.json()['Tasks']:
            task_date = datetime.strptime(task['created_at'], "%a, %d %b %Y %H:%M:%S %Z")
            tasks.append([ str(task['id']), task['name'], task['desc'], 
                           task_date, task['status'] ])

        headers = ["Id", "task_name", "task_desc", "created_at", "status"]
        table = tabulate(tasks, headers=headers, tablefmt="grid", numalign="center")
        
        print(table)

    elif id and all is False:
        req = requests.get(api_url + "tasks" + "/" + str(id))

        print(f"get task details with id {id}")
        if req.status_code == 404:
            print(req.json())
            return
        
        task = req.json()['task']
        task_date = datetime.strptime(task['created_at'], "%a, %d %b %Y %H:%M:%S %Z")
        data = [[str(task['id']), task['task_name'], task['task'], 
                 task_date, task['status']]]
        
        headers = ["Id", "task_name", "task_desc", "created_at", "status"]
        table = tabulate(data, headers=headers, tablefmt="grid", numalign="center")
        print(table)

@task.command('add', help='add new task')
@click.option('--name', '-n', type=str, help='add task name')
@click.option('--desc', '-d', type=str, help='add task description')
def add(name, desc):
    if name is None or desc is None:
        print("enter task --name <name> and --desc <desc> to add")
        return
    
    data = {'name': name, 'desc': desc}
    req = requests.post(api_url + 'tasks', json=data)
    print(req.json())

@task.command('update', help='update task')
@click.option('--id', '-i', type=str, help='add task id')
@click.option('--name', '-n', type=str, help='add task name')
@click.option('--desc', '-d', type=str, help='add task description')
@click.option('--status', '-s', type=str, help='add task description')
def update(id, name, desc, status):
    if id and status:
            data = {'id': id, 'status': status}
            req = requests.put(api_url + 'tasks' + '/' + str(id), json=data)
            print(req.json())
            return

    elif id is None and name is None and desc is None or \
        name is None and desc is None or name is None or desc is None:
        print("enter task --id <id> and --name <name> --desc <desc> to update")
        return

    data = {'id': id, 'name': name, 'desc': desc}
    req = requests.put(api_url + 'tasks' + '/' + str(id), json=data)
    print(req.json())


@task.command('delete', help='delete task')
@click.option('--id', '-i', type=str, help='add task id')
def delete(id):
    if id is None:
        print("enter task --id to delete")
        return
    req = requests.delete(api_url + 'tasks' + '/' + str(id))
    print(req.json())


@note.command('get', help='get note details')
@click.option('--id', help='specify note id to get')
@click.option('--all', is_flag=True, help='get all notes')
def get(id, all):
    if id is None and all is False:
        print("enter --id <id> to get specific note or --all to get all notes")
    elif id is None and all is True:
        req = requests.get(api_url + "notes")

        if len(req.json()['Notes']) == 0:
            print(req.json())
            return
        
        print("got all notes for you")
        notes = []
        for note in req.json()['Notes']:
            notes.append([str(note['id']), note['name'], note['desc']])

        headers = ["Id", "note_name", "note_desc"]
        table = tabulate(notes, headers=headers, tablefmt="grid", numalign="center")
        
        print(table)

    elif id and all is False:
        req = requests.get(api_url + "notes" + "/" + str(id))

        print(f"get note details with id {id}")
        if req.status_code == 404:
            print(req.json())
            return
        
        note = req.json()['note']
        data = [[str(note['id']), note['note_name'], note['note']]]
        headers = ["Id", "note_name", "note_desc"]
        table = tabulate(data, headers=headers, tablefmt="grid", numalign="center")
        print(table)

@note.command('add', help='add new note')
@click.option('--name', '-n', type=str, help='add note name')
@click.option('--desc', '-d', type=str, help='add note description')
def add(name, desc):
    if name is None or desc is None:
        print("enter note --name <name> and --desc <desc> to add")
        return
    
    data = {'name': name, 'desc': desc}
    req = requests.post(api_url + 'notes', json=data)
    print(req.json())

@note.command('update', help='update note')
@click.option('--id', '-i', type=str, help='add note id')
@click.option('--name', '-n', type=str, help='add note name')
@click.option('--desc', '-d', type=str, help='add note description')
def update(id, name, desc):
    if id is None and name is None and desc is None or \
        name is None and desc is None or name is None or desc is None:
        print("enter note --id <id> and --name <name> --desc <desc> to update")
        return
    
    data = {'id': id, 'name': name, 'desc': desc}
    req = requests.put(api_url + 'notes' + '/' + str(id), json=data)
    print(req.json())

@note.command('delete', help='delete note')
@click.option('--id', '-i', type=str, help='add note id')
def delete(id):
    if id is None:
        print("enter note --id to delete")
        return
    req = requests.delete(api_url + 'notes' + '/' + str(id))
    print(req.json())


cli.add_command(task)
cli.add_command(note)


if __name__ == '__main__':
    cli()
