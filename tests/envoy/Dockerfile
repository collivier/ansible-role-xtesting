FROM opnfv/functest-kubernetes-cnf:v1.32

USER root
RUN cd /tmp && git clone https://github.com/cnti-testcatalog/testsuite.git && \
    mv testsuite/example-cnfs/envoy /src && \
    rm -rf testsuite
USER xtesting
COPY testcases.yaml /etc/xtesting/testcases.yaml
