#!/bin/bash

function all() {
  migrate
  pip3 install -r requirements.txt
  python3 -m safety check -r requirements.txt
  python3 manage.py check
  static
  setup
}

function run_tests() {
  python3 manage.py test
}

function clean() {
  rm -rf main/migrations/*
  files=$(find . -name "__pycache__")
  files2=$(find . -iregex ".*\.\(pyc\)")
  rm -rf "${files2}"
  rm -rf "${files}"
}

function migrate() {
  pwd
  python3 manage.py makemigrations main
  python3 manage.py makemigrations
  python3 manage.py migrate
}

function makemigrations() {
  python3 manage.py makemigrations main
  python3 manage.py makemigrations
}

function static() {
  python3 manage.py collectstatic --no-input
}

function run() {
  python3 manage.py runserver 0.0.0.0:1234
}

function reset_migrations() {
  python3 manage.py migrate --fake main
  python3 manage.py showmigrations
  rm -rf main/migrations
  python3 manage.py migrate --fake-initial
  python3 manage.py showmigrations
}

function setup() {
  python3 manage.py setup
}

function shell() {
  python3 manage.py shell
}

function check() {
  # We're going to ignore E1101, since Django exposes members to Model classes
  # that PyLint can't see.
  clear && \
   black . && \
   run_tests && \
   pylint main --disable=E1101,W0613,R0903,C0301,C0114,C0115,C0116,R0801
}

function gunicorn_run() {
  gunicorn fennelapi.wsgi:application --bind 0.0.0.0:1234
}

case "$1" in

check)
  check
  ;;

startapp)
  python3 manage.py startapp "$2"
  ;;

clean)
  clean
  ;;

migrate)
  migrate
  ;;

test)
  run_tests
  ;;

run)
  run
  ;;

setup)
  setup
  ;;

init-all-run)
  all
  gunicorn_run
  ;;

docker-init-all)
  check
  all
  ;;

all-run)
  check
  all
  run
  ;;

all)
  all
  ;;

reset_migrations)
  reset_migrations
  ;;

makemigrations)
  makemigrations
  ;;

shell)
  shell
  ;;

esac
