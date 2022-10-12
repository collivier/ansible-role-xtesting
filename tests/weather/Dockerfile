FROM alpine:3.16

ADD . /src/
RUN apk --no-cache add --update python3 py3-pip py3-wheel git py3-lxml && \
    git init /src && pip3 install /src
COPY testcases.yaml /etc/xtesting/testcases.yaml
CMD ["run_tests", "-t", "all"]
