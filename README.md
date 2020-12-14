#       spam-detector-api


spam-detector-api is a REST interface to model trained to detect spam phone calls. The training project is here: https://github.com/beratakuzum/spam-detector-train

### Dependencies and Libraries

  - Python 3.8
  - Flask
  - MongoDB

# How to Run?
First thing to do is to put the trained model file in the trained_model folder with the name spam-detector-model.pickle .Also, users used to make predictions have to be in spam_detector database and users table in mongodb.

###### You can run the project either using docker-compose or just from command line.

- The configuration settings must be in a .env file residing in the project's root directory. Also, MongoDB connection string that is in 'src/services/mongodb.py' should be changed if you are not running the flask app and mongodb with docker-compose. You can run the project simply by creating a virtual environment, install the packages in the requirements.txt file and run this command:
```sh
$ python run.py
```

- To run the project via docker-compose, run these commands:
```sh
$ docker-compose build
$ docker-compose up
```
# API Documentation
### Register
The use the prediction api, you have to be registered with a username and password.
##### Request
```
Method: POST
Url: /api/register
Body: {
    "username": "berat",
    "password":"12345"
}
```
##### Successful Response
```
Response Code: 201
Body: {
    "access_token": "xxx",
    "refresh_token":"xxx",
    "user_id": "xxx"
}
```

### Login
Get an access token and refresh token
##### Request
```
Method: GET
Url: /api/login
params:
    username: berat,
    password: 12345
```
##### Successful Response
```
Response Code: 200
Body: {
    "access_token": "xxx",
    "refresh_token":"xxx",
    "user_id": "xxx"
}
```
### Refresh Token
Get a new access token and refresh token
##### Request
```
Method: GET
Url: /api/refresh-token
headers = {
    "access_token": "xxx",
    "refresh_token": "xxx"
}
```
##### Successful Response
```
Response Code: 200
Body: {
    "access_token": "xxx",
    "refresh_token":"xxx"
}
```
### Prediction
*Note: To test the prediction api, you first have to insert the users in data/call_history.csv file into the users collection in mongodb's spam_detector database.*

This endpoint predicts if a user is spam or not.
##### Request
```
Method: GET
Url: /api/prediction/<user_id>
headers = {
    "Authentication": "access_token"
}
```
##### Successful Response
```
Response Code: 200
Body: {
    "user_id": "user_id",
    "is_spam": true
}
```