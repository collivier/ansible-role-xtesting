# Xtesting Ansible Role

Xtesting have leveraged on Functest efforts to provide a reference testing framework. To learn more about Xtesting: http://xtesting.readthedocs.io/en/latest/


# Variables

- `prefix`: (default `/data`) Base directory for the persistent storage of the containers (Jenkins, Mongo, etc.)
- `use_proxy`: (default: `false`) When true, uses a proxy for those tasks that require Internet connectivity. Requires to set also `http_proxy` and `https_proxy`.


## Site.yml example:

```
---
- hosts: 127.0.0.1
  roles:
    - role: ../ansible-role-xtesting
      project: weather
      repo: 127.0.0.1
      dport: 5000
      gerrit:
      suites:
        - container: weather
          tests:
            - humidity
            - pressure
            - temp
            - half
      jenkins_deploy: true
      jenkins_configure: true
      minio_deploy: true
      radosgw_deploy: false
      mongo_deploy: true
      testapi_deploy: true
      testapi_configure: true
      registry_deploy: true
      postgres_deploy: true
      cachet_deploy: true
      cachet_configure: true
```

## Inventory file example:

```yaml
---
xtesting:
  hosts:
    127.0.0.1:
      ansible_user: xtesting
      ansible_python_interpreter: auto
  vars:
    http_proxy: http://10.113.55.36:8080
    https_proxy: http://10.113.55.36:8080
    use_proxy: true
```

# TO-DO:
- Don't escalate privileges for Docker tasks

