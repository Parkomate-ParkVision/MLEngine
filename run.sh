#!/bin/bash
modes="start-dev stop-dev interactive-dev check-syntax"
mode=$1
project_name="ml-template"

if [ "$project_name" == "*****" ]; then
    echo "Please Update the Project Name in run.sh"
    exit 0;
fi

if [ "$mode" == "" ]; then
    echo "Invalid mode.\n mode must be one of: ${modes}"
elif [ "$mode" == "start-dev" ]; then
    docker-compose -p ${project_name}-dev -f docker-compose.yml build
    docker-compose -p ${project_name}-dev -f docker-compose.yml up -d
elif [ "$mode" == "stop-dev" ]; then
    docker-compose -p ${project_name}-dev -f docker-compose.yml down
elif [ "$mode" == "interactive-dev" ]; then
    docker exec -it --user root microservice-dev bash
elif [ "$mode" == "check-syntax" ]; then
    docker exec -it --user root microservice-dev flake8 .
else
    echo "Invalid mode.\n mode must be one of: ${modes}"
fi
