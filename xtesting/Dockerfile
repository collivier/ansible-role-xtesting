FROM opnfv/xtesting

COPY site.yml /src/site.yml
RUN apk --no-cache add --update openssh && \
  ansible-galaxy install collivier.xtesting && \
  ansible-galaxy collection install ansible.posix community.general \
    community.grafana community.kubernetes community.docker \
    community.postgresql
COPY testcases.yaml /usr/lib/python3.9/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
