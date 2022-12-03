# ereader

## required docker images
- pdf to html conversion: [pdf2htmlEX](https://github.com/coolwanglu/pdf2htmlEX)
- search engine: [typesense.org](https://typesense.org/docs/guide/install-typesense.html#%F0%9F%93%A5-download-install)
  
```
$ docker pull klokoy/pdf2htmlex
$ docker pull typesense/typesense:0.23.1
```

## setup workspace
- setup ereader (flask)
```
$ cd ereader                        
$
$ python3 -m venv venv
$ source venv/bin/activate      <-- run this after each pull to ensure
$ pip install -r venv.txt       <-- all required libs are installed
$ deactivate
$ 
$ mkdir ./typesense-data
$ export TYPESENSE_API_KEY=xyz  <-- this should be same as .env
$ docker run -p 8108:8108 -v$(pwd)/typesense-data:/data typesense/typesense:0.23.1 \
  --data-dir /data --api-key=$TYPESENSE_API_KEY --enable-cors
```
<!-- 
$ pip freeze > venv.txt             <-- (not required) list virtual env libraries 
-->

- setup ereader-ui (angular)
```
$ cd ereader-ui
$ npm i
```

## run the project (dev: http://localhost:4200/)
- run ereader
```
$ cd ereader
$ source venv/bin/activate
$ flask --app app.py --debug run
```
- run ereader-ui
```
$ cd ereader-ui
$ ng serve
```
