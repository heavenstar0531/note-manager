# Simple Notes Manager in Python 

Simple Notes Manager (API, console client) written in Python with web.py.

## API documentation
    https://notesmanager.docs.apiary.io/

## Video with web client example
    https://vimeo.com/84667505

## Running the application in development mode
    cd api
    uwsgi -c uwsgi.ini
    (press CTRL+C to close the application)

## Running the application in the background
    cd api
    uwsgi -c uwsgi.ini --daemonize application.log

## Turning off the application running in the background
    cd api
    uwsgi --stop uwsgi.pid
    
## Running console client
    cd console-client
    python notes-manager-client.py -h
