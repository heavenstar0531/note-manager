# Simple Notes Manager in Python (API, console client) 

## Running the application in development mode
$ uwsgi -c uwsgi.ini
(press CTRL+C to close the application)

## Running the application in the background
$ uwsgi -c uwsgi.ini --daemonize application.log

## Turning off the application running in the background
$ uwsgi --stop uwsgi.pid
