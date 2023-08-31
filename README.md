# iam
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub](https://img.shields.io/badge/fastapi-v.0.89.1-blue)
![GitHub](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)
![GitHub](https://img.shields.io/badge/license-MIT-blue)

---
#### Disclaimer: I am using a cookie-cutter code provided by fastapi-mvc as a base template to write code. But all the business logic, Models, and controllers are all written by me.

### Documentation

## Step 1) Setup docker and docker-compose 
Install docker: https://docs.docker.com/engine/install/ubuntu/ 

Install docker-compose : https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04

## Step 2)
cd into the root directory of the project

Run ```docker-compose up -d --build```
This will install the flask application and also download the mongo and redis containers required for this app to work

## Step 3)
Now you can test the application by importing the IAM.postman_collection file in the root directory into postman

Start with the health_check route and make sure the response is as follows
```{
    "status": true,
    "message": "Healthcheck success",
    "data": {
        "app": true,
        "database": true,
        "redis": true
    }
}
```
This ensures that the app and all its dependencies are running as expected, if any of these come back as false that means that specific service is not running as expected, or the fast API application is not able to connect with it.

## Step 4)
Once the deployment is complete and ensured it is running as expected, we need to first create a user using the method user_create. The sample request bodies are present in the Postman collection

Then we have to create a token using the token_get API. This will give a response as follows
```{
    "status": true,
    "message": "User authenticated",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsImtpZCI6IkhQZTA5UG1weUJYbGxoRVhSU2JqT0k4WmZlUEk3TXl5IiwidHlwIjoiSldUIn0.eyJzdWIiOiJwcmFub3kiLCJleHAiOjE2OTMzNzI1NDl9.9feu_f0pC4hqHMsvR9c7eI3Srvkv6NrJayclR_IPtRs",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsImtpZCI6IkhQZTA5UG1weUJYbGxoRVhSU2JqT0k4WmZlUEk3TXl5IiwidHlwIjoiSldUIn0.eyJzdWIiOiJwcmFub3kiLCJleHAiOjE2OTMzNzQyODl9.Ha10ck5Euvid09yLcyE_BZF-IltHeON3kTPoLLok_hc",
        "token_type": "bearer"
    }
}
```
From this, we have to use the access_token value for all the nonpublic API's

Note: For the ease of use of this project, I have removed authentication from some of  the RBAC-related APIs so that demoing the functionality of this backend becomes easier. Since I am using a refresh token mechanism, the actual access_token expires very fast and a custom client application logic has to be used to leverage the power of refresh tokens, which is not so straightforward to do using Postman.


### Step 5)
Now we have to create actions -> resources -> permission -> role in this same order as the role is dependent on permissions, permission is dependent on resources, and so on. 

Note : The project is not a 100% due to the time restrictions, we have to map the role to a user ideally and then attach then extract the permissions of that role and add it onto the JWT payload of the user. When the user tries to make a request to the IAM app or any other app registered in this IAM micro service, the application looks through the permissions of the user using a middleware used to extract the JWT payload and gets the permission related information and then allows or rejects the request.

This can be done on an APP level or API level or a mix of both. On the APP level, the middleware can reject the person requesting does not have access to the APP at all. Then on an API level we can check whether the user has access to use the API. I believe this approach reduces the complexity of the middleware a lot and gives us a lot of control and flexibility to write custom rules on an API level.

