# task10

This is task and note management with locally started small rest api and simple cli client.
Same app will be written in different languages/frameworks for learning and comparing.

I have intended to use any stack on api side. after starting rest api app, we will be able to use cli tool to manage our personal tasks and notes.

#### ToDos:
- Impletement same rest api written in flask for all other stacks
- Add status column for tasks
- implement cli tool version in other languages also.


```bash
click, tabulate and requests should be installed in order to use cli tool.

python3 client.py 
Usage: client.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.       

Commands:
  note  Note management
  task  Task management
```

We have 2 subcommands, note and task for managing them from cli accordingly.

How to manage subcommands, example notes:

```bash
python3 client.py note
Usage: client.py note [OPTIONS] COMMAND [ARGS]...

  Note management

Options:
  --help  Show this message and exit.

Commands:
  add     add new note
  delete  delete note
  get     get note details
  update  update note
```

To see help menu use --help
```bash
python3 client.py note get --help

Usage: client.py note get [OPTIONS]     

  get note details

Options:
  --id TEXT  specify note id to get     
  --all      get all notes
  --help     Show this message and exit.
```

To get all notes
```bash
python3 client.py note get --all

{'Notes': []}
```

Let us add new note
```bash
python3 client.py note add --help

Usage: client.py note add [OPTIONS]

  add new note

Options:
  -n, --name TEXT  add note name
  -d, --desc TEXT  add note description       
  --help           Show this message and exit.
```

We need to give name and desc to add new note
```bash
python3 client.py note add --name test_note01 --desc "write document for new feature"

{'msg': 'note with id 1 added successfully'}

python3 client.py note add --name google_toolbox_url --desc "https://toolbox.googleapps.com/apps/dig/"

{'msg': 'note with id 2 added successfully'}
```

to see all notes
```bash
python3 client.py note get --all

got all notes for you
+------+--------------------+------------------------------------------+
|  Id  | note_name          | note_desc                                |
+======+====================+==========================================+
|  1   | test_note01        | write document for new feature           |
+------+--------------------+------------------------------------------+
|  2   | google_toolbox_url | https://toolbox.googleapps.com/apps/dig/ |
+------+--------------------+------------------------------------------+
```
To see specific note, ex: 2
```bash
python3 client.py note get --id 2

get note details with id 2
+------+--------------------+------------------------------------------+
|  Id  | note_name          | note_desc                                |
+======+====================+==========================================+
|  2   | google_toolbox_url | https://toolbox.googleapps.com/apps/dig/ |
+------+--------------------+------------------------------------------+
```
To delete note, let us see its --help
```bash
python3 client.py note delete --help

Usage: client.py note delete [OPTIONS]

  delete note

Options:
  -i, --id TEXT  add note id
  --help         Show this message and exit.
```
Let us delete note 2
```bash
python3 client.py note delete --id 2

{'msg': 'note with 2 deleted successfully'}
```

We now have only note with id 1
```bash
python3 client.py note get --all

got all notes for you
+------+-------------+--------------------------------+
|  Id  | note_name   | note_desc                      |
+======+=============+================================+
|  1   | test_note01 | write document for new feature |
+------+-------------+--------------------------------+
```

Update subcommand help
```bash
python3 client.py note update --help

Usage: client.py note update [OPTIONS]        

  update note

Options:
  -i, --id TEXT    add note id
  -n, --name TEXT  add note name
  -d, --desc TEXT  add note description       
  --help           Show this message and exit.
```
let us update note 1
```bash
python3 client.py note update --id 1 --name "test_note_UPDATED" --desc "UPDATE: dont write doc, done by teammate"

{'message': 'Note  updated'}
```
To see update
```bash
python3 client.py note get --id 1

get note details with id 1
+------+-------------------+------------------------------------------+
|  Id  | note_name         | note_desc                                |
+======+===================+==========================================+
|  1   | test_note_UPDATED | UPDATE: dont write doc, done by teammate |
+------+-------------------+------------------------------------------+
```
