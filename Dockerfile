FROM ubuntu:latest
LABEL authors="gabri"

ENTRYPOINT ["top", "-b"]