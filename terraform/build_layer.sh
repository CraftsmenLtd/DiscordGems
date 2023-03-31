#!/bin/bash

# Exit if any of the intermediate steps fail
set -e

{
    eval "$(jq -r '@sh "export DESTINATION_DIR=\(.DESTINATION_DIR) MODULE_DIR=\(.MODULE_DIR) ZIPFILE_NAME=\(.ZIPFILE_NAME)"')"
    DESTINATION_DIR=${DESTINATION_DIR:-$PWD}
    MODULE_DIR=${MODULE_DIR:-$PWD}
    ZIPFILE_NAME=${ZIPFILE_NAME:-layer}
    
    TARGET_DIR=$DESTINATION_DIR/$ZIPFILE_NAME
    mkdir -p "$TARGET_DIR"/python
    
    (cd "$MODULE_DIR"/../ && pip3 install -r requirements.txt -t "$TARGET_DIR"/python)
    (cd "$TARGET_DIR" && zip -r "$TARGET_DIR".zip ./* -x "*.dist-info*" -x "*__pycache__*" -x "*.egg-info*")
    
    rm -r "$TARGET_DIR"
} &> /dev/null

jq -n --arg zipfile "$TARGET_DIR".zip '{"zipfile_path": $zipfile}'
