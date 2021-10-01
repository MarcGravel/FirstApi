# Animal API

Animal API allows users to get, post, patch, and delete from a database of animals.

## Requirements

mariadb,
flask

```bash
pip install mariadb
pip install flask
```

## How to use

This is not a live api. Must use your own server and database. The database on this project is available for import as well.


# Endpoint: /animals


## "GET": No params required
Returns a complete list of animals from the database 

## "POST": Data is required
```json
{"animal_name": "lizard"}
```
Requires JSON request with "animal_name" as key and then whatever animal you please.

Will not accept repeat animals or empty strings

## "PATCH": Data is required
```json
{"id": "2", "animal_name": "lizard"}
```
Requires JSON request which includes "id" and "animal_name". This will replace current animal name with requested value on matching id.

Id must be valid and animal name must be unique.

## "DELETE": Data is required
```json
{"animal_name": "lizard"}
```
Requires JSON request with "animal_name" as key and then whatever animal you please.

Will only delete valid animals that exist in database


# Contributing
No Contributions 
