# Casting Agency

## Introduction
This is my capstone project for the full-stack developer Nanodegree. The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 

## Getting Started
### Base URL
You can run the app locally or in Heroku:
- Locally: http://127.0.0.1:5000/
- Heroku: https://lama-capston1.herokuapp.com/ 

### Installing Dependencies
Python 3.8
Follow instructions to install the latest version of python here (https://docs.python.org/3/)

PIP Dependencies
Install dependencies by running:
```pip install -r requirements.txt```
This will install all of the required packages within the requirements.txt file.

*All needed variables are saved in setup.sh*


### Authentication: 
I used Auth0 tokens for the authentication. There are three roles for the casting agency:
**Casting Assistant**
- Can view actors and movies
**Casting Director**
- Can view actors and movies
- Add or delete an actor from the database
- Modify actors or movies
**Executive Producer**
- Can view actors and movies
- Add or delete an actor from the database
- Modify actors or movies
- Add or delete a movie from the database

## Test
You can test the app by running the test_app.py or using Postman collection.

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "Resource Not Found"
}
```

### Error Types and Messages
The Casting Agency app will return the below error types when requests fail:
- 404: Resource Not Found
- 422: Not Processable
- 405: Method Not Allowed
- 400: Bad Request
- 500: Internal Server Error

## Resource Endpoint Library
### GET '/movies'
* Genreal
    * Fetches a dictionary of movies
    * Request Arguments: None
    * Returns: An object that contains movies array, and a success boolean value.
* Sample: `curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/movies`

```
{
  "movies": [
    {
      "id": 1,
      "release_date": "Wed, 20 Jan 2016 00:00:00 GMT",
      "title": "Split"
    },
    {
      "id": 2,
      "release_date": "Tue, 07 Jan 2020 00:00:00 GMT",
      "title": "Bad Boys for Life"
    },
    {
      "id": 3,
      "release_date": "Fri, 02 Apr 2021 00:00:00 GMT",
      "title": "No Time to Die"
    },
    {
      "id": 4,
      "release_date": "Fri, 16 Jul 2021 00:00:00 GMT",
      "title": "Uncharted"
    },
    {
      "id": 5,
      "release_date": "Fri, 01 Jan 2021 00:00:00 GMT",
      "title": "We Can Be Heroes"
    }
  ],
  "success": true
}
```


### GET '/actors'
* Genreal
    * Fetches a dictionary of actors
    * Request Arguments: None
    * Returns: An object that contains actors array, and a success boolean value.
* Sample: `curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/actors`

```
{
  "actors": [
    [
      {
        "age": 41,
        "gender": "Male",
        "id": 1,
        "name": "James McAvoy"
      },
      {
        "age": 52,
        "gender": "Male",
        "id": 2,
        "name": "Will Smith"
      },
      {
        "age": 24,
        "gender": "Female",
        "id": 3,
        "name": "Tati Gabrielle"
      },
      {
        "age": 35,
        "gender": "Female",
        "id": 4,
        "name": "L\u201aa Seydoux"
      },
      {
        "age": 27,
        "gender": "Female",
        "id": 5,
        "name": "Taylor Dooley"
      }
    ]
  ],
  "success": true
}
```

### POST '/movies'
* General
    * Creates a new movie
    * Request Arguments: None
    * Returns: An object that contains a success boolean value and the created movie.
* Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"title\":\"A Quiet Place Part II\",\"release-date\":\"2021-04-01\"}"`
```
{
  "movie": {
    "id": 10,
    "release_date": "Thu, 01 Apr 2021 00:00:00 GMT",
    "title": "A Quiet Place Part II"
  },
  "success": true
}
```

### POST '/actors'
* General
    * Creates a new actor
    * Request Arguments: None
    * Returns: An object that contains a success boolean value and the created actor.
* Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"name\":\"Emily Blunt\",\"age\":\"37\",\"gender\":\"Female\"}"`
```
{
  "actor": {
    "age": 37,
    "gender": "Female",
    "id": 8,
    "name": "Emily Blunt"
  },
  "success": true
}
```


### PATCH '/movies/1'
* General
    * Updates the specified movie
    * Request Arguments: None
    * Returns: An object that contains a success boolean value and the updated movie.
* Sample: `curl http://127.0.0.1:5000/movies/1 -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"title\":\"New Movie\"}"`
```
{
  "movie": {
    "id": 1,
    "release_date": "Wed, 20 Jan 2016 00:00:00 GMT",
    "title": "New Movie"
  },
  "success": true
}
```

### PATCH '/actors/1'
* General
    * Updates the specified actor
    * Request Arguments: None
    * Returns: An object that contains a success boolean value and the updated actor.
* Sample: `curl http://127.0.0.1:5000/actors/1 -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"name\":\"New Name\"}"`
```
{
  "actor": {
    "age": 37,
    "gender": "Male",
    "id": 41,
    "name": "New Name"
  },
  "success": true
}
```

### DELETE '/movies/2'
* Genreal
    * Removes the specified movie
    * Request Arguments: The movie's ID
    * Returns: An object than contains a success boolean value and the ID of the deleted movie.
* Sample: `curl -X DELETE -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/movies/2`
```
{
  "deleted": 2,
  "success": true
}
```

### DELETE '/actors/2'
* Genreal
    * Removes the specified actor
    * Request Arguments: The actor's ID
    * Returns: An object than contains a success boolean value and the ID of the deleted actor.
* Sample: `curl -X DELETE -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/actors/2`
```
{
  "deleted": 2,
  "success": true
}
```
