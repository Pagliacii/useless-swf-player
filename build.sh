#!/bin/bash

set -eu
set -o pipefail

DESTINATION="releases/useless-swf-player.tar.gz"

usage() {
    echo -e "The build script to generate the release tar file"
    echo -e ""
    echo -e "./build.sh"
    echo -e "\t-h | --help    show this message and exit"
    echo -e ""
}

while [ $# -ne 0 ] && [ "$1" != "" ]; do
    PARAM="$(printf "%s\n" "$1" | awk -F= '{print $1}')"
    VALUE="$(printf "%s\n" "$1" | sed 's/^[^=]*=//g')"
    if [ "$VALUE" = "$PARAM" ] && [ $# -gt 1 ]; then
        shift
        VALUE=$1
    fi

    case $PARAM in
        -h | --help)
            usage
            exit
            ;;
        *)
            echo -e "ERROR: unknown parameter \"$PARAM\""
            usage
            exit 1
            ;;
    esac
    shift
done

[ -d "releases" ] || mkdir releases
[ -z ${DESTINATION} ] && rm -f ${DESTINATION}
tar --exclude="app.db" \
    --exclude="app.log" \
    --exclude="package.json" \
    --exclude="postcss.config.js" \
    --exclude="tailwind.config.js" \
    --exclude="yarn.lock" \
    --exclude="yarn-error.log" \
    --exclude="__pycache__" \
    --exclude="app/__pycache__" \
    --exclude="node_modules" \
    --exclude="*.swf" \
    --exclude="releases" \
    --exclude="build.sh" \
    --exclude=".gitignore" \
    --exclude=".git" \
    --exclude="./css" \
    --exclude="assets" \
    -czvf ${DESTINATION} .