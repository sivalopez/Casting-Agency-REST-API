# Casting Agency 
The Casting Agency application is responsible for creating movies and actors as well as managing them.
This project has been created as a capstone project as part of the Udacity's Fullstack Developer Nano Degree (FSND).
By completing this project, I am applying the skills learnt during the course of this Nano Degree such as 
- utilizing SQLAlchemy to model database and run queries in PostgreSQL,
- implementing RESTful API endpoints using Flask as well as including unit tests,
- enabling authentication and Role Based Access Contol using Auth0 and
- deploying this API on Heroku.

## Getting Started
### Authentication
Instructions for setting up authentication for testing endpoints at live application endpoint.
- Create an Auth0 tenant domain.
- Create a new Single Page Web Application.
  - Configure "Application Login URI"
  - Configure "Allowed Callback URLs"
- Create a new API.
  - Enable RBAC
  - Enable Add Permissions in the Access Token
- Create API permission for the following:
  - get:movies
  - post:movies
  - patch:movies
  - delete:movies
  - get:actors
  - post:actors
  - patch:actors
  - delete:actors
- Create user roles and assign permissions.
  - Casting Director - Assign all permissions except delete:movies.
  - Executive Producer - Assign all permissions.
- Create two users and assign roles.
  - Create a user and assign Casting Director role.
  - Create another user and assign Executive Producer role.
- Generate JWTs for both the users.
- Update setup.sh with correct AUTH0_DOMAIN, ALGORITHMS and API_AUDIENCE.

### Accessing the hosted API
Application is hosted live at http://FSND-Capstone-Casting-Agency.herokuapp.com

### Local Development
### Installing Dependencies
Project dependencies, local development and hosting instructions
```
pip install -r requirements.txt
```

### Running the server
Detailed instructions for scripts to install any project dependencies and to run the development server.


## API Reference
### Error Handling
Errors are returned as JSON objects.
- Sample: `curl -X PATCH http://127.0.0.1:5000/movies/2 -d '{"title": "Hello Movie", "release_date": "2020-12-31"}' -H 'Content-Type: application/json' -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdJM0x0SEdpYnVuMmFaOXVKSHJuRyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2Fwc3RvbmUtc2lsby5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0MzY3NDYyMWRhM2YwMDY4NzkzYWY0IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3lfYXBpIiwiaWF0IjoxNTk4Njk3MTk4LCJleHAiOjE1OTg3ODM1OTgsImF6cCI6ImNoZnhTVUtXQWlBUUtyVGxheG5tR0dRdnljTEx0Z2FoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.cJUmYVs72O0oDt0i1iaCXyxNa5dSABoEei2CYwamm29fXETgBDu5LRn0VKm2U0ZSWSoPcjr2LY9ffTApZn9UW0c6Ibpr9lTL7foozNQqBAbPt0YGumLTyVv34D9YCh6GZ_qZtjfKq1t1Z04TTRZaKOUiDnohVFwCDYTmx48RDCTk9vGkDPm6OD0Apf12sw0XgZfSCbK0MVCLlnT16TSbCzsexDZLwpi7fhFGbtTws_6kQco-e26Z_yzFy14IGUjF8RvBIK_rkzaswPTIdxj2-_5hI_i-9Bdp0wPTrk1Wd4zHl0vpnRMH3Piou_B9uIMfn9HH1LlEVodyinSPCITalA'`
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
- token_expired: Token expired.
- missing_authorization_header: Authorization header is expected.
- invalid_header: Authorization header must start with 'Bearer'.
- invalid_header: Authorization header must be bearer token.
- invalid_header: Token not found.
- invalid_header: Authorization malformed.
- invalid_header: Unable to parse authentication token.
- invalid_header: Unable to find the appropriate key.
- invalid_header: Authorization header must include permissions.
- invalid_claims: Incorrect claims. Please, check the audience and issuer.
- unauthorized_request: No permission to perform the request.

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
- Sample: `curl -X POST http://127.0.0.1:5000/movies -d '{"title": "Hello Movie", "release_date": "2020-12-31"}' -H 'Content-Type: application/json' -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdJM0x0SEdpYnVuMmFaOXVKSHJuRyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2Fwc3RvbmUtc2lsby5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0MzY3NDYyMWRhM2YwMDY4NzkzYWY0IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3lfYXBpIiwiaWF0IjoxNTk4Njk3MTk4LCJleHAiOjE1OTg3ODM1OTgsImF6cCI6ImNoZnhTVUtXQWlBUUtyVGxheG5tR0dRdnljTEx0Z2FoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.cJUmYVs72O0oDt0i1iaCXyxNa5dSABoEei2CYwamm29fXETgBDu5LRn0VKm2U0ZSWSoPcjr2LY9ffTApZn9UW0c6Ibpr9lTL7foozNQqBAbPt0YGumLTyVv34D9YCh6GZ_qZtjfKq1t1Z04TTRZaKOUiDnohVFwCDYTmx48RDCTk9vGkDPm6OD0Apf12sw0XgZfSCbK0MVCLlnT16TSbCzsexDZLwpi7fhFGbtTws_6kQco-e26Z_yzFy14IGUjF8RvBIK_rkzaswPTIdxj2-_5hI_i-9Bdp0wPTrk1Wd4zHl0vpnRMH3Piou_B9uIMfn9HH1LlEVodyinSPCITalA'`
```
{
  "id": 1, 
  "success": true
}
```
#### PATCH /movies
- General:
  - Updates the movie with the given JSON data containing movie title and release date for the given movie id.
  - Request Arguments: data
  - Returns a dictionary with the updated movie id and success status of true.
- Sample: `curl -X PATCH http://127.0.0.1:5000/movies/1 -d '{"title": "Fifth Element", "release_date": "1994-07-16"}' -H 'Content-Type: application/json' -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdJM0x0SEdpYnVuMmFaOXVKSHJuRyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2Fwc3RvbmUtc2lsby5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0MzY3NDYyMWRhM2YwMDY4NzkzYWY0IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3lfYXBpIiwiaWF0IjoxNTk4Njk3MTk4LCJleHAiOjE1OTg3ODM1OTgsImF6cCI6ImNoZnhTVUtXQWlBUUtyVGxheG5tR0dRdnljTEx0Z2FoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.cJUmYVs72O0oDt0i1iaCXyxNa5dSABoEei2CYwamm29fXETgBDu5LRn0VKm2U0ZSWSoPcjr2LY9ffTApZn9UW0c6Ibpr9lTL7foozNQqBAbPt0YGumLTyVv34D9YCh6GZ_qZtjfKq1t1Z04TTRZaKOUiDnohVFwCDYTmx48RDCTk9vGkDPm6OD0Apf12sw0XgZfSCbK0MVCLlnT16TSbCzsexDZLwpi7fhFGbtTws_6kQco-e26Z_yzFy14IGUjF8RvBIK_rkzaswPTIdxj2-_5hI_i-9Bdp0wPTrk1Wd4zHl0vpnRMH3Piou_B9uIMfn9HH1LlEVodyinSPCITalA'`
```
{
  "id": "1", 
  "success": true
}
```
#### DELETE /movies
- General:
  - Deletes the movie for the given movie id.
  - Returns a dictionary with the deleted movie id and success status of true.
- Sample: `curl -X DELETE http://127.0.0.1:5000/movies/2 -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdJM0x0SEdpYnVuMmFaOXVKSHJuRyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2Fwc3RvbmUtc2lsby5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0MzZjYTZkYmVlZWIwMDZkZGIyNTQ1IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3lfYXBpIiwiaWF0IjoxNTk4Njk3MjYzLCJleHAiOjE1OTg3ODM2NjMsImF6cCI6ImNoZnhTVUtXQWlBUUtyVGxheG5tR0dRdnljTEx0Z2FoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.h06icY-f-sDIXXH8-ktCAh5CkQ5N6Dgoe0JPmzt4M_zXX9R9fi1TPvNcEzPlr6Vji8kuIALwiBO4FVcC-p9DJwkvDr1r0mtSWa7nWeHkJwpGoo9H-lWT0RDB8Tt3sET18dI3395eXnH7z50gw1gNQJr6f8WcXVwLh49ISS1EK1_dnmgF00QMGUb1Nz6le-iUTi43zuqGLX4HUKySR9gqOAaNgcvx2-UoWYE_52HRFMBB36jK4vyaoMEtaBYc2LBxWPYkCvRWZvvg7t_CiGe-LMXFoVfiqkmdEMGVgYY5-vfza1kg4CXEDFeychLvHinMYnIjQv0Y8vGe98JJ85lA2A'`
```
{
  "id": "2", 
  "success": true
}

```
#### GET /actors
- General: 
  - Fetches a list of actors in which each actor is a dictionary of id, name, age and gender.
  - Returns an object with a list of actors and success status of true.
- Sample: `curl -X GET http://127.0.0.1:5000/actors`
```
{
  "actors": [
    {
      "age": 40, 
      "gender": "Female", 
      "id": 1, 
      "name": "Julia Roberts"
    },  
    {
      "age": 34, 
      "gender": "Male", 
      "id": 2, 
      "name": "Henry Williams"
    }
  ], 
  "success": true
}
```
#### POST /actors
- General: 
  - Adds the new actor with the given JSON data containing actor's name, age and gender.
  - Request Arguments: data
  - Returns a dictionary with the new actor id and success status of true.
- Sample: `curl -X POST http://127.0.0.1:5000/actors -d '{"name": "Henry Williams", "age": 34, "gender": "Male"}' -H 'Content-Type: application/json' -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdJM0x0SEdpYnVuMmFaOXVKSHJuRyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2Fwc3RvbmUtc2lsby5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0MzY3NDYyMWRhM2YwMDY4NzkzYWY0IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3lfYXBpIiwiaWF0IjoxNTk4Njk3MTk4LCJleHAiOjE1OTg3ODM1OTgsImF6cCI6ImNoZnhTVUtXQWlBUUtyVGxheG5tR0dRdnljTEx0Z2FoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.cJUmYVs72O0oDt0i1iaCXyxNa5dSABoEei2CYwamm29fXETgBDu5LRn0VKm2U0ZSWSoPcjr2LY9ffTApZn9UW0c6Ibpr9lTL7foozNQqBAbPt0YGumLTyVv34D9YCh6GZ_qZtjfKq1t1Z04TTRZaKOUiDnohVFwCDYTmx48RDCTk9vGkDPm6OD0Apf12sw0XgZfSCbK0MVCLlnT16TSbCzsexDZLwpi7fhFGbtTws_6kQco-e26Z_yzFy14IGUjF8RvBIK_rkzaswPTIdxj2-_5hI_i-9Bdp0wPTrk1Wd4zHl0vpnRMH3Piou_B9uIMfn9HH1LlEVodyinSPCITalA'`
```
{
  "id": 2, 
  "success": true
}
```
#### PATCH /actors
- General:
  - Updates the actor with the given JSON data containing actor's name, age and gender for the given actor id.
  - Request Arguments: data
  - Returns a dictionary with the updated actor id and success status of true.
- Sample: `curl -X PATCH http://127.0.0.1:5000/actors/1 -d '{"name": "Julia Roberts"}' -H "Content-Type: application/json" -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdJM0x0SEdpYnVuMmFaOXVKSHJuRyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2Fwc3RvbmUtc2lsby5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0MzY3NDYyMWRhM2YwMDY4NzkzYWY0IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3lfYXBpIiwiaWF0IjoxNTk4Njk3MTk4LCJleHAiOjE1OTg3ODM1OTgsImF6cCI6ImNoZnhTVUtXQWlBUUtyVGxheG5tR0dRdnljTEx0Z2FoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.cJUmYVs72O0oDt0i1iaCXyxNa5dSABoEei2CYwamm29fXETgBDu5LRn0VKm2U0ZSWSoPcjr2LY9ffTApZn9UW0c6Ibpr9lTL7foozNQqBAbPt0YGumLTyVv34D9YCh6GZ_qZtjfKq1t1Z04TTRZaKOUiDnohVFwCDYTmx48RDCTk9vGkDPm6OD0Apf12sw0XgZfSCbK0MVCLlnT16TSbCzsexDZLwpi7fhFGbtTws_6kQco-e26Z_yzFy14IGUjF8RvBIK_rkzaswPTIdxj2-_5hI_i-9Bdp0wPTrk1Wd4zHl0vpnRMH3Piou_B9uIMfn9HH1LlEVodyinSPCITalA'`
```
{
  "id": "1", 
  "success": true
}
```
#### DELETE /actors
- General:
  - Deletes the actor for the given actor id.
  - Returns a dictionary with the deleted actor id and success status of true.
- Sample: `curl -X DELETE http://127.0.0.1:5000/actors/2 -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdJM0x0SEdpYnVuMmFaOXVKSHJuRyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2Fwc3RvbmUtc2lsby5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0MzY3NDYyMWRhM2YwMDY4NzkzYWY0IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3lfYXBpIiwiaWF0IjoxNTk4Njk3MTk4LCJleHAiOjE1OTg3ODM1OTgsImF6cCI6ImNoZnhTVUtXQWlBUUtyVGxheG5tR0dRdnljTEx0Z2FoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.cJUmYVs72O0oDt0i1iaCXyxNa5dSABoEei2CYwamm29fXETgBDu5LRn0VKm2U0ZSWSoPcjr2LY9ffTApZn9UW0c6Ibpr9lTL7foozNQqBAbPt0YGumLTyVv34D9YCh6GZ_qZtjfKq1t1Z04TTRZaKOUiDnohVFwCDYTmx48RDCTk9vGkDPm6OD0Apf12sw0XgZfSCbK0MVCLlnT16TSbCzsexDZLwpi7fhFGbtTws_6kQco-e26Z_yzFy14IGUjF8RvBIK_rkzaswPTIdxj2-_5hI_i-9Bdp0wPTrk1Wd4zHl0vpnRMH3Piou_B9uIMfn9HH1LlEVodyinSPCITalA'`
```
{
  "id": "2", 
  "success": true
}
```
