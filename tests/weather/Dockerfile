FROM alpine:3.12

ADD . /src/
RUN apk --no-cache add --update python3 py3-pip py3-wheel git && \
    git init /src && pip3 install /src
COPY testcases.yaml /usr/lib/python3.8/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
