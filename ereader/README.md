# ereader

a simple ereader (prototype) to demonstrate the search functionality (using typesense as the engine)

please check [search.py](./apps/search.py) for the typesense configuration, indexing, and search function. you may use a different typesense document format containing more meta data. in our case, we included course_id, section_id, ..., and page_num.

## required docker images

- pdf to html conversion: [pdf2htmlEX](https://github.com/coolwanglu/pdf2htmlEX), this is used to convert pdf files to html pages.
- search engine: [typesense.org](https://typesense.org/docs/guide/install-typesense.html#%F0%9F%93%A5-download-install), this is used as the search engine.

  ```
  $ docker pull klokoy/pdf2htmlex
  $ docker pull typesense/typesense:0.23.1
  ```

## setup project

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

- make sure your docker is running (required for pdf2html conversion)
- run typesense docker
  ```
  $ cd ereader
  $ export TYPESENSE_API_KEY=xyz  <-- same as .env
  $ docker run -p 8108:8108 -v$(pwd)/typesense-data:/data typesense/typesense:0.23.1 \
    --data-dir /data --api-key=$TYPESENSE_API_KEY --enable-cors
  ```
- run ereader
  ```
  $ cd ereader
  $ source venv/bin/activate
  $ flask --app app.py --debug run
  ```
