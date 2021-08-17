FROM alpine:3.14

ADD . /src/
RUN apk --no-cache add --update python3 py3-pip py3-wheel git libxml2 libxslt && \
    apk --no-cache add --virtual .build-deps --update python3-dev build-base libxml2-dev libxslt-dev && \
    git init /src && pip3 install /src && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python3.9/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
