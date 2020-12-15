#  Deploy your own Xtesting CI/CD toolchains

For the time being, the ansible playbooks automatically deploy the next
components (they are configured to allow running testcases directly):
- Jenkins
- Minio
- S3www
- MongoDB
- TestAPI
- Docker Registry
- PostgreSQL
- Cachet
- GitLab
- InfluxDB
- Grafana

Here are the default TCP ports which have to be free or updated (see
https://github.com/collivier/ansible-role-xtesting/blob/master/defaults/main.yml):
- Jenkins: 8080
- Minio: 9000
- S3www: 8181
- TestAPI: 8000
- Docker Registry: 5000
- PostgreSQL: 5432
- Cachet: 8001
- GitLab: 80
- InfluxDB: 8086
- Grafana: 3000

Xtesting is designed to allow running your own containers based on that
framework even out of the Infrastracture domain (e.g. ONAP).

Be free to list them into suites!

## Install dependencies

Xtesting Continous integration helper depends on the 3 next packages:
- python-virtualenv
- docker.io
- git


Install dependencies (Debian):
```bash
sudo apt install python-virtualenv docker.io git
```

Install dependencies (CentOS):
```bash
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install python-virtualenv docker-ce git
```

Please note the next two points depending on the GNU/Linux distributions and
the network settings:
- SELinux: you may have to add --system-site-packages when creating the
  virtualenv ("Aborting, target uses selinux but python bindings
  (libselinux-python) aren't installed!")
- Proxy: you may set your proxy in env for Ansible and in systemd for Docker
  https://docs.docker.com/config/daemon/systemd/#httphttps-proxy


## Add Xtesting user (Optional)

It should be noted the ansible user must be allowed to run tasks with the root
priviledes via sudo and to access the docker socket for a few specific tasks.

NOPASSWD may be an help but you could rather prompt the password (e.g. sudo ls)
before deploying the toolchains

Create Xtesting user (optional)
```bash
sudo useradd -s /bin/bash -m xtesting
echo "xtesting ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/xtesting
sudo usermod -aG sudo xtesting
sudo usermod -aG docker xtesting
sudo su - xtesting
```

## Deploy your Xtesting CI/CD toolchain (Jenkins)

Deploy your own Xtesting toolchain
```bash
virtualenv xtesting
. xtesting/bin/activate
pip install ansible
ansible-galaxy install collivier.xtesting
git clone https://gerrit.opnfv.org/gerrit/functest-xtesting functest-xtesting-src
ansible-playbook functest-xtesting-src/ansible/site.yml
deactivate
rm -rf functest-xtesting-src xtesting
```

Access to the different dashboards:
- Jenkins: http://127.0.0.1:8080/ (admin/admin)
- Minio: http://127.0.0.1:9000/ (xtesting/xtesting)
- S3www: http://127.0.0.1:8181/
- TestAPI: http://127.0.0.1:8000

## Deploy your Xtesting CI/CD toolchain (GitLab CI/CD)

Deploy your own Xtesting toolchain
```bash
virtualenv xtesting
. xtesting/bin/activate
pip install ansible
ansible-galaxy install collivier.xtesting
git clone https://gerrit.opnfv.org/gerrit/functest-xtesting functest-xtesting-src
pushd functest-xtesting-src
patch -p1 << EOF
diff --git a/ansible/site.yml b/ansible/site.yml
index 8fa19688..a4260cd8 100644
--- a/ansible/site.yml
+++ b/ansible/site.yml
@@ -2,6 +2,9 @@
 - hosts: 127.0.0.1
   roles:
     - role: collivier.xtesting
+      gitlab_deploy: true
+      jenkins_deploy: false
+      jenkins_load_jobs: false
       builds:
         dependencies:
           - repo: _
EOF
popd
ansible-playbook functest-xtesting-src/ansible/site.yml
deactivate
rm -rf functest-xtesting-src xtesting
```

Access to the different dashboards:
- GitLab: http://127.0.0.1/ (xtesting/xtesting)
- Minio: http://127.0.0.1:9000/ (xtesting/xtesting)
- S3www: http://127.0.0.1:8181/
- TestAPI: http://127.0.0.1:8000

## Deploy your Functest CI/CD toolchain

Deploy your own Functest toolchain
```bash
virtualenv functest
. functest/bin/activate
pip install ansible
ansible-galaxy install collivier.xtesting
git clone https://gerrit.opnfv.org/gerrit/functest functest-src
ansible-playbook functest-src/ansible/site.yml
deactivate
rm -rf functest-src functest
```

Note: By default, the latest version is considered, if you want to create a
gate for a specific Functest version (i.e. a specific OpenStack version), you
can checkout the right branch.

Deploy your own Functest Hunter toolchain
```bash
virtualenv functest
. functest/bin/activate
pip install ansible
ansible-galaxy install collivier.xtesting
git clone https://gerrit.opnfv.org/gerrit/functest functest-src
(cd functest-src && git checkout -b stable/hunter origin/stable/hunter)
ansible-playbook functest-src/ansible/site.yml
deactivate
rm -rf functest-src functest
```

As a reminder the version table can be summarized as follows:

| Functest releases | OpenStack releases |
|:-----------------:|:------------------:|
| Hunter            | Rocky              |
| Iruya             | Stein              |
| Jerma             | Train              |
| Kali              | Ussuri             |
| Leguer            | Victoria           |
| Master            | next Wallaby       |


Here are the default Functest tree as proposed in Run Alpine Functest containers (master):
- /home/opnfv/functest/openstack.creds
- /home/opnfv/functest/images

## Deploy your CNTT API Compliance CI/CD toolchain


Deploy your own Functest toolchain
```bash
virtualenv functest
. functest/bin/activate
pip install ansible
ansible-galaxy install collivier.xtesting
git clone https://gerrit.opnfv.org/gerrit/functest functest-src
(cd functest-src && git checkout -b stable/hunter origin/stable/hunter)
ansible-playbook functest-src/ansible/site.cntt.yml
deactivate
rm -rf functest-src functest
```

Note: By default, CNTT Baldy is considered, if you want to create a gate for a
specific CNTT version, you can checkout the right branch.

Deploy your own Functest toolchain
```bash
virtualenv functest
. functest/bin/activate
pip install ansible
ansible-galaxy install collivier.xtesting
git clone https://gerrit.opnfv.org/gerrit/functest functest-src
(cd functest-src && git checkout -b stable/jerma origin/stable/jerma)
ansible-playbook functest-src/ansible/site.cntt.yml
deactivate
rm -rf functest-src functest
```

As a reminder the version table can be summarized as follows:

| Functest releases | OpenStack releases | CNTT releases |
|:-----------------:|:------------------:|:-------------:|
| Hunter            | Rocky              | Baldy         |
| Iruya             | Stein              | Baldy         |
| Jerma             | Train              | Baraque       |
| Kali              | Ussuri             | Baraque       |
| Leguer            | Victoria           | Baraque       |
| Master            | next Wallaby       | Baraque       |

Here are the default Functest tree as proposed in Run Alpine Functest
containers (master):
- /home/opnfv/functest/openstack.creds
- /home/opnfv/functest/images


## Deploy your Functest Kubernetes CI/CD toolchain

Deploy your own Functest toolchain
```bash
virtualenv functest-kubernetes
. functest-kubernetes/bin/activate
pip install ansible
ansible-galaxy install collivier.xtesting
git clone https://gerrit.opnfv.org/gerrit/functest-kubernetes functest-kubernetes-src
ansible-playbook functest-kubernetes-src/ansible/site.yml
deactivate
rm -rf functest-kubernetes-src functest-kubernetes
```

Note: By default, the latest version is considered, if you want to create a
gate for a specific Functest version (i.e. a specific Kubernetes version), you
can checkout the right branch:

Deploy your own Functest Kubernetes Hunter toolchain
```bash
virtualenv functest-kubernetes
. functest-kubernetes/bin/activate
pip install ansible
ansible-galaxy install collivier.xtesting
git clone https://gerrit.opnfv.org/gerrit/functest-kubernetes functest-kubernetes-src
(cd functest-kubernetes-src && git checkout -b stable/hunter origin/stable/hunter)
ansible-playbook functest-kubernetes-src/ansible/site.yml
deactivate
rm -rf functest-kubernetes-src functest-kubernetes
```

As a reminder the version table can be summarized as follows:

| Functest releases | Kubernetes releases |
|:-----------------:|:-------------------:|
| Hunter            | v1.13               |
| Iruya             | v1.15               |
| Jerma             | v1.17               |
| Kali              | v1.19               |
| Leguer            | v1.20 (rolling)     |
| Master            | v1.20 (rolling)     |

Here is the default Functest Kubernetes tree as proposed in Run kubernetes
testcases (master):
- /home/opnfv/functest-kubernetes/config

## Deploy your own CI/CD toolchain from scratch

Write hello.robot
```
*** Settings ***
Documentation    Example using the space separated plain text format.
Library          OperatingSystem

*** Variables ***
${MESSAGE}       Hello, world!

*** Test Cases ***
My Test
    [Documentation]    Example test
    Log    ${MESSAGE}
    My Keyword    /tmp

Another Test
    Should Be Equal    ${MESSAGE}    Hello, world!

*** Keywords ***
My Keyword
    [Arguments]    ${path}
    Directory Should Exist    ${path}
```

Write Dockerfile
```
FROM opnfv/xtesting

COPY hello.robot hello.robot
COPY testcases.yaml /usr/lib/python3.8/site-packages/xtesting/ci/testcases.yaml
```

Write testcases.yaml
```yaml
---
tiers:
    -
        name: hello
        order: 1
        description: ''
        testcases:
            -
                case_name: hello
                project_name: helloworld
                criteria: 100
                blocking: true
                clean_flag: false
                description: ''
                run:
                    name: 'robotframework'
                    args:
                        suites:
                            - /hello.robot
```

Build your container
```bash
sudo docker build -t 127.0.0.1:5000/hello .
```

Run your new container
```bash
sudo docker run -t 127.0.0.1:5000/hello
```

```
+-------------------+--------------------+---------------+------------------+----------------+
|     TEST CASE     |      PROJECT       |      TIER     |     DURATION     |     RESULT     |
+-------------------+--------------------+---------------+------------------+----------------+
|       hello       |     helloworld     |     hello     |      00:00       |      PASS      |
+-------------------+--------------------+---------------+------------------+----------------+
```

Write site.yml
```yaml
---
- hosts:
    - 127.0.0.1
  roles:
    - role: collivier.xtesting
      project: helloworld
      repo: 127.0.0.1
      dport: 5000
      gerrit:
      suites:
        - container: hello
          tests:
            - hello
```

Deploy your own Xtesting toolchain
```bash
virtualenv xtesting
. xtesting/bin/activate
pip install ansible
ansible-galaxy install collivier.xtesting
ansible-playbook site.yml
deactivate
PLAY RECAP ****************************************************************
127.0.0.1                  : ok=17   changed=11   unreachable=0    failed=0
```

Publish your container on your local repository
```bash
sudo docker push 127.0.0.1:5000/hello
```

## That's all folks!
