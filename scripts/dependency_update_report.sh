#!/bin/sh

echo "Project directory is ${1}"

cd "${1}"

mvn help:effective-pom  -Doutput=effective-pom.xml

docker run --rm -it -v "${1}":/project afrunt/maven-toys python3 effective_pom_to_dependency_report.py --effective_pom_file /project/effective-pom.xml --report_file /project/dependency-report.json
docker run --rm -it -v "${1}":/project afrunt/maven-toys python3 dependency_to_update_report.py --dependency_report_file /project/dependency-report.json --report_file /project/update-report

