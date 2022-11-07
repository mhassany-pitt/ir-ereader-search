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

## setup typesense

- install docker image
```
$ docker pull typesense/typesense:0.23.1
```

- run docker image

use the same TYPESENSE_API_KEY as in .env file.

```
$ cd ./ereader
$ export TYPESENSE_API_KEY=xyz
$ mkdir $(pwd)/typesense-data
$ docker run -p 8108:8108 -v$(pwd)/typesense-data:/data typesense/typesense:0.23.1 \
  --data-dir /data --api-key=$TYPESENSE_API_KEY --enable-cors
```

- install typesense python library
```
$ pip install typesense
```