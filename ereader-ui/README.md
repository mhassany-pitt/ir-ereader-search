# ereader-ui

ui app for the simple [ereader](../ereader/README.md)

typesense provide data adapter for the algolia search ui to work with typesense. however, due to version incompability we decided to create a simple search field using [primeng autocomplete component](http://primefaces.org/primeng/autocomplete).

please check the reader [component](./src/app/reader/reader.component.ts), and [template](./src/app/reader/reader.component.html) to see how this has been done.

## setup project

- make sure you have [nodejs](https://nodejs.org/en/) installed.
  ```
  $ cd ereader-ui
  $ npm i
  ```

## run the project (dev: http://localhost:4200/)

- run ui
  ```
  $ cd ereader-ui
  $ ng serve
  ```
