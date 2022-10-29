# ereader

## install deps
```
$ cd ereader
$ python3 -m venv venv              <-- (once) create virtual env
$ source venv/bin/activate          <-- activate virtual env

$ pip install -r venv.txt           <-- install virtual env libraries
$ deactivate                        <-- deactivate virtual env
```
<!-- 
$ pip freeze > venv.txt             <-- (not required) list virtual env libraries 
-->

## run the project (dev: http://localhost:5000/)
```
$ cd ereader
$ source venv/bin/activate          <-- activate virtual env
$ flask --app app.py --debug run    <-- run the app
$ deactivate                        <-- deactivate virtual env
```