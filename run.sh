#!/bin/bash

set -eu
set -o pipefail

usage() {
    echo -e "Run the application with some options"
    echo -e ""
    echo -e "./run.sh [options]"
    echo -e "\t--help              show this message and exit"
    echo -e "\t-d|--dev            running in development mode"
    echo -e "\t-p|--prod           running in production mode"
    echo -e "\t--processes <num>   use <num> processes (only for production mode)"
    echo -e "\t--threads <num>     use <num> threads (only for production mode)"
    echo -e "\t-h|--host <host>    the host to bind to"
    echo -e "\t--port <port>       the port to bind to"
}

MODE="dev"
HOST="127.0.0.1"
PORT=5000
PROCESSES=4
THREADS=2
while [ $# -ne 0 ] && [ "$1" != "" ]; do
    PARAM="$(printf "%s\n" "$1" | awk -F= '{print $1}')"
    VALUE="$(printf "%s\n" "$1" | sed 's/^[^=]*=//g')"
    if [ "$VALUE" = "$PARAM" ] && [ $# -gt 1 ]; then
        shift
        VALUE=$1
    fi

    case $PARAM in
        --help)
            usage
            exit
            ;;
        -d|--dev)
            MODE="dev"
            ;;
        -p|--prod)
            MODE="prod"
            HOST="0.0.0.0"
            PORT=9000
            ;;
        --processes)
            PROCESSES=$VALUE
            ;;
        --threads)
            THREADS=$VALUE
            ;;
        -h|--host)
            HOST=$VALUE
            ;;
        --port)
            PORT=$VALUE
            ;;
        *)
            echo "ERROR: unknown parameter \"$PARAM\""
            usage
            exit 1
            ;;
    esac
    shift
done

if [ "${MODE}" = "prod" ]; then
    pipenv run uwsgi \
        --http ${HOST}:${PORT} \
        --wsgi-file ./wsgi.py \
        --callable app \
        --processes ${PROCESSES} \
        --threads ${THREADS}
else
    yarn run watch:css &
    FLASK_APP=wsgi.py FLASK_ENV=development pipenv run flask run --host ${HOST} --port ${PORT}
fi