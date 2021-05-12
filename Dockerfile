FROM oraclelinux:7-slim

RUN echo "Building..." \
    && yum update -y \
    && yum upgrade -y \
    && yum install -y python3 python-pip \
    && pip3 install jsonpickle

