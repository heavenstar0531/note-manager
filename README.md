# Simple Notes Manager in Python (API, console client, web client) 

## Uruchomienie aplikacji w trybie developerskim
$ uwsgi -c uwsgi.ini
(press CTRL+C to close the application)

## Uruchomienie aplikacji w tle
$ uwsgi -c uwsgi.ini --daemonize application.log

## Wyłączenie aplikacji działającej w tle
$ uwsgi --stop uwsgi.pid
