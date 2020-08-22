# FSND Capstone Casting Agency Project
Udacity Fullstack Developer Nano Degree capstone project.
## Motivation for the project

## Getting Started
### Installing Dependencies
Project dependencies, local development and hosting instructions
### Running the server
Detailed instructions for scripts to install any project dependencies and to run the development server.

## API Reference
### RBAC controls
### Error Handling
Errors are returned as JSON objects.
- Sample: `curl -X PATCH http://127.0.0.1:5000/actors/2`
```
{
  "error": 404, 
  "message": "Resource Not Found", 
  "success": false
}
```
The API will return these error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable

### Endpoints
#### GET /movies
- General: 
  - Fetches a list of movies in which each movie is a dictionary of id, title and release_date.
  - Returns an object with a list of movies and success status of true.
- Sample: `curl -X GET http://127.0.0.1:5000/movies`
```
{
  "movies": [
    {
      "id": 1, 
      "release_date": "Thu, 31 Dec 2020 00:00:00 GMT", 
      "title": "Spirited Away"
    }, 
    {
      "id": 2, 
      "release_date": "Thu, 31 Dec 2020 00:00:00 GMT", 
      "title": "Hello Movie"
    }
  ], 
  "success": true
}
```
#### POST /movies
- General: 
  - Adds the new movie with the given JSON data containing movie title and release date.
  - Request Arguments: data
  - Returns a dictionary with the new movie id and success status of true.
- Sample: `curl -X POST http://127.0.0.1:5000/movies -d '{"title": "Hello Movie", "release_date": "2020-12-31"}' -H 'Content-Type: application/json'`
```
{
  "id": 2, 
  "success": true
}
```
#### PATCH /movies
- General:
  - Updates the movie with the given JSON data containing movie title and release date for the given movie id.
  - Request Arguments: data
  - Returns a dictionary with the updated movie id and success status of true.
- Sample: `curl -X PATCH http://127.0.0.1:5000/movies/2 -d '{"title": "Hello world 2!"}' -H "Content-Type: application/json"`
```
{
  "id": "2", 
  "success": true
}
```
#### DELETE /movies
- General:
  - Deletes the movie for the given movie id.
  - Returns a dictionary with the deleted movie id and success status of true.
- Sample: `curl -X DELETE http://127.0.0.1:5000/movies/2`
```
{
  "id": "2", 
  "success": true
}

```
#### GET /actors
#### POST /actors
#### PATCH /actors
#### DELETE /actors
