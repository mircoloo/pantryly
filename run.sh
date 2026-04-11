#!/bin/bash
PATH=./node_modules/.bin:$PATH

WORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

function install {
    npm install
}

function build {
    webpack
}

function start {
    build # Call task dependency
    python -m SimpleHTTPServer 9000
}

function test {
    mocha test/**/*.js
}

function default {
    # Default task to execute
    help
}

function run_uvicorn:inventory {
    source "$WORK_DIR/microservices/inventory-service/.venv/bin/activate"
    echo "$WORK_DIR/microservices/inventory-service/.venv/bin/activate"
    uvicorn app.main:app \
  --app-dir "$WORK_DIR/microservices/inventory-service" \
  --port 8000 --host 0.0.0.0 --reload
}


function help {
    echo "$0 <task> <args>"
    echo "Tasks:"
    compgen -A function | cat -n
}

TIMEFORMAT="Task completed in %3lR"
time ${@:-default}