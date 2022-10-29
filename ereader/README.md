# ereader

- make sure you have installed the latest version of Flask globally
``` 
pip3 install -U Flask
``` 

# run the project (dev)
```
$ cd ereader

$ python3 -m venv venv              <-- (once) create virtual env

$ source venv/bin/activate          <-- activate virtual env

$ pip install -r venv.txt           <-- install virtual env libraries
$ pip freeze > venv.txt             <-- (not required) list virtual env libraries

$ flask --app app.py --debug run    <-- run the app

$ deactivate                        <-- deactivate virtual env
```