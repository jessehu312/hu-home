# Hu's Home
Hu's home (pronounced - who's home) is an app to track if everybody in a family is home
This repo contains Hu's home websocket server and a simple web client

# Setup

## Initial
```
py -3 -m venv venv
venv\Scripts\activate
pip install 
```

## Running Server
```
venv\Scripts\activate
set FLASK_APP=hu-home
set FLASK_ENV=development
flask run
```

## Try it out
http://127.0.0.1:5000/
