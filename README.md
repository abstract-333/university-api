# Project for university
Rest API project for university, that emluate university system):
<br/>

## Running on:
* Windows 11

* Python 3.11.4 or higher

* PostgreSQL

## How to run

### Install from git:

#### Using GitFlic:

```shell
$ git clone https://gitflic.ru/project/abstract-333/university-api.git

$ cd university-api
```

### Create and activate virutal environment:

```shell
$ python -m venv .venv

$ .\.venv\Scripts\activate
```

### Install dependencies:

```shell
$ pip install -r requirements.txt
```

### Make migration for database:

_<strong>
First Create database under "name".
<br>
Add this name and other properties to .env.prod file.
</strong>_
<br>
<br>

```shell
$ alembic upgrade heads
```

### Run App:

* #### Using Make:
```shell
$ make run
```

* #### Without Make:
```shell
$ uvicorn --factory src.app:app --reload
```


## How to run