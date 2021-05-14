FROM oraclelinux:7-slim

RUN echo "Building..." \
    && yum update -y \
    && yum upgrade -y \
    && yum install -y python3 python-pip \
    && pip3 install jsonpickle requests

WORKDIR /

ADD mt /mt/
ADD effective_pom_to_dependency_report.py /
ADD dependency_to_update_report.py /



