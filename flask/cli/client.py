import click

@click.command()
@click.option('--name', help='Name of task or note')
@click.option('--desc', prompt='task or name description', help='we')
def hello(count, name):
    """Cli tool for tasks and notes api management"""
    for _ in range(count):
        click.echo(f'Hello, {name}!')

if __name__ == '__main__':
    hello()