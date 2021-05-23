FROM ubuntu:latest

LABEL version="0.1.0"

WORKDIR /srv

RUN apt update && \
    apt install -y python3-pip libssl-dev

# install package locally (for development)
RUN python3 -m pip install .
# install python package from pypi
# RUN python3 -m pip install Wellness-Bot

# run wellness bot
CMD [ "start" ]