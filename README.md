# Drones Test

## Build command

`docker-compose build`

## Run command

`docker-compose up -d`

Next go to [Api doc](http://localhost:8000/doc/) for the api definitions and explication

- The program will load some data for testing like drones, medications and one user account
- Use JWT for authentication
- Default user credentials are:
    - username: admin_drones
    - password: admin_drones

    - Request:
    ```bash
    curl --request POST 'http://localhost:8000/token/obtain/' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "username": "admin_drones",
            "password": "admin_drones"
        }'
    ```
    - Response:
    `{"access": "xxxxxxx", "refresh": "xxxxxxx"}`  
    
    - `access` is the token for authentication (lifetime: 5 minutes), `refresh` is the token for refreshing the token

    - Example Request:
    ```bash
    curl --location --request GET 'http://localhost:8000/drones/list' \
        --header 'Authorization: Bearer _access_token_'
    ```

Requeriments:
 - Registering a drone POST http://localhost:8000/drones/list/
 - Loading a drone with medication items POST http://localhost:8000/drones/load/
 - Checking loaded medication items for a given drone GET http://localhost:8000/medications/loaded/{uuid}/ (program saves all medications loaded by drones for log history and uses a flag 'delivered' to known this load was delivered, must be only one load undelivered for each drone.

 - Checking available drones for loading GET http://localhost:8000/drones/available/
 - Check drone battery level for a given drone GET http://localhost:8000/drones/battery/{uuid}

 - Periodic task to log drones battery level is executed every hour and save data, for cheking the history go to GET http://localhost:8000/drones/log/

## Test command 

`docker-compose exec backend python manage.py test apps/`

