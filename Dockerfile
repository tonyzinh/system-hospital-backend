FROM ubuntu:latest
LABEL authors="enton"

ENTRYPOINT ["top", "-b"]