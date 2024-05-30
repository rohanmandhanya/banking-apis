### Objective

While modern banks have evolved to serve a plethora of functions, at their core, banks must provide certain basic features. Today, your task is to build the basic HTTP API for one of those banks! Imagine you are designing a backend API for bank employees. It could ultimately be consumed by multiple frontends (web, iOS, Android etc).


### Run dev[Local]

I have wrapped the backend application in Docker system which will help us scale it easily.
It consist of two major parts, one is our backend application and another is a database on which we store out information

- Bank 
- Bank DB 


#### Dependencies
We only require a docker engine to run our application. To install [docker](https://docs.docker.com/engine/install/) follow steps mention in it.

#### Run application 
```
docker compose up
```

#### Test application
Needs to have a python env setup, than run `pip install -r requirements.txt`

Run (pytest)[https://docs.pytest.org/en/8.2.x/] to test the whole application(*api endpoints and core logic*)
```
pytest
```

#### Documentation
The application is well documented and can be find on localhost:8000/documentation once you have spinned up the docker compose

#### Application details

You can use localhost:8000/docs to test endpoints on swagger platform. 

You need to create a user to test it. I have pre-populated some users as request and you can login them using `fake@test.com` password would be `fake`.

Once you have logged in, you can use all the api which are secured


### Tasks

- Implement assignment using:
  - Language: **Python**
  - Framework: **any framework except Django** 
- There should be API routes that allow them to:
  - Create a new bank account for a customer, with an initial deposit amount. A
    single customer may have multiple bank accounts.
  - Transfer amounts between any two accounts, including those owned by
    different customers.
  - Retrieve balances for a given account.
  - Retrieve transfer history for a given account.
- Write tests for your business logic