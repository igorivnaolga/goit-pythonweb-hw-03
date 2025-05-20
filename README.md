# Project Description

This project is a simple web application implemented using Python’s built-in http.server module. It demonstrates basic web server functionality, HTML form processing, static file serving, and templating with Jinja2.

## Task Overview

This project is based on starter files from this repository:
https://github.com/GoIT-Python-Web/FullStack-Web-Development-hw3

## Features

Serves two HTML pages:

/ → index.html

/message → message.html (includes a form)

Handles static files: style.css, logo.png

Processes form input from message.html and saves it to a local JSON file storage/data.json

Adds each message with a timestamp as a key (using datetime.now())

Returns a custom error.html page for 404 errors

Runs on port 3000

Provides a /read route that displays all stored messages using a Jinja2 template

## Bonus Task (Optional)

Create a Dockerfile and run the app in a Docker container

Use Docker volumes to persist storage/data.json outside the container
