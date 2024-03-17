import requests
import click

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
        print("make get request to get all tasks")
        req = requests.get(api_url + "tasks")
        print(req.json())
    elif id and all is False:
        print(f"get task details with id {id}")
        req = requests.get(api_url + "tasks" + "/" + str(id))
        print(req.json())

@task.command('add', help='add new task')
def add():
    click.echo('Add new task')

@task.command('update', help='update task')
def add():
    click.echo('Update task')

@task.command('delete', help='delete task')
def add():
    click.echo('Delete task')


@note.command('get', help='get note details')
@click.option('--id', help='specify note id to get')
@click.option('--all', is_flag=True, help='get all notes')
def get(id, all):
    if id is None and all is False:
        print("enter --id <id> to get specific note or --all to get all notes")
    elif id is None and all is True:
        print("make get request to get all notes")
        req = requests.get(api_url + "notes")
        print(req.json())
    elif id and all is False:
        print(f"get note details with id {id}")
        req = requests.get(api_url + "notes" + "/" + str(id))
        print(req.json())

@note.command('add', help='add new note')
def add():
    click.echo('Add new note')

@note.command('update', help='update note')
def add():
    click.echo('Update note')

@note.command('delete', help='delete note')
def add():
    click.echo('Delete note')

cli.add_command(task)
cli.add_command(note)

if __name__ == '__main__':
    cli()
