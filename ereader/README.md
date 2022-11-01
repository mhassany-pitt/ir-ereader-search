# ereader



## install deps
```
$ cd ereader
$ python3 -m venv venv              <-- (once) create virtual env
$ source venv/bin/activate          <-- activate virtual env

$ pip install -r venv.txt           <-- install virtual env libraries
$ deactivate                        <-- deactivate virtual env
```

make sure you have [pdf2htmlEX docker image - 1.23GB by Kim Lokøy kim.lokoy@gmail.com](https://github.com/coolwanglu/pdf2htmlEX) running - we use it for pdf2html conversion. 

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