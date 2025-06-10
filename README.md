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

Note that [running MongoDB 5.0+ requires _avx_ CPU instruction set](https://www.mongodb.com/docs/manual/administration/production-notes/#x86_64)
that is usually shipped in all recent _x86_ hardware processors.
Though, it may not be available in your virtualized environments.
For example, Qemu _avx_ support is only available [since version 7.2](https://github.com/nodkz/mongodb-memory-server/issues/710#issuecomment-1297462935)
and must be explicitly enabled (e.g. with the argument _-cpu max_).

You can check the presence of the _avx_ CPU instruction set on your processor
with the following command.
```bash
grep '^processor\|^flags.* avx' /proc/cpuinfo
```

## Add Xtesting user (Optional)

It should be noted the ansible user must be allowed to run tasks with the root
privileges via sudo. NOPASSWD may be an help but you could rather prompt the
password (e.g. sudo ls) before deploying the toolchains.

Create Xtesting user
```bash
sudo useradd -s /bin/bash -m xtesting
echo "xtesting ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/xtesting
sudo su - xtesting
```

## Create a virtualenv (Optional)

It should be noted that ansible 2.10 or newer is required and that a few python
packages are installed via pip. Therefore you may create a python virtualenv.
It's worth mentioning that CentOS forces us to give the virtual environment
access to the global site-packages (libselinux-python wouldn't be available).

Create Xtesting virtualenv (Debian)
```bash
sudo apt update && sudo apt install virtualenv -y
virtualenv xtesting -p python3 --system-site-packages
. xtesting/bin/activate
pip install ansible
```

Create Xtesting virtualenv (CentOS)
```bash
sudo yum install epel-release -y
sudo yum install virtualenv -y
virtualenv xtesting -p python3 --system-site-packages
. xtesting/bin/activate
pip install ansible
```

## Install dependencies

Xtesting Continous Integration helper only depends on ansible>=2.9. In case of
Debian Buster, ansible should be installed via pip as the official Debian
package is too old. It should be installed via pip in Ubuntu as well to avoid
mismatches between ansible and virtualenv Ubuntu packages. It should be noted
that git is only needed for the following playbooks.

Install dependencies (Debian Bullseye):
```bash
sudo apt update -y && sudo apt install git -y
[ -z "$VIRTUAL_ENV" ] && sudo apt install python3-pip -y && sudo pip3 install ansible
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
```

**Install dependencies (Debian Bookworm):**
```bash
sudo apt update -y && sudo apt install git -y
[ -z "$VIRTUAL_ENV" ] && sudo apt install ansible -y
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
```

Install dependencies (Debian Trixie and Sid):
```bash
sudo apt update -y && sudo apt install git -y
[ -z "$VIRTUAL_ENV" ] && sudo apt install ansible -y
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
```

Install dependencies (Ubuntu Focal):
```bash
sudo apt update -y && sudo apt install git -y
[ -z "$VIRTUAL_ENV" ] && sudo apt install python3-pip -y && sudo pip3 install ansible
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
ansible-galaxy collection install -f community.docker
```

Install dependencies (Ubuntu Jammy):
```bash
sudo apt update -y && sudo apt install git -y
[ -z "$VIRTUAL_ENV" ] && sudo apt install python3-pip -y && sudo pip3 install ansible
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
```

**Install dependencies (Ubuntu Noble):**
```bash
sudo apt update -y && sudo apt install git -y
[ -z "$VIRTUAL_ENV" ] && sudo apt install ansible -y
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
```

Install dependencies (Ubuntu Oracular):
```bash
sudo apt update -y && sudo apt install git -y
[ -z "$VIRTUAL_ENV" ] && sudo apt install ansible -y
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
ansible-galaxy collection install -f community.docker
```

Install dependencies (Ubuntu Plucky):
```bash
sudo apt update -y && sudo apt install git -y
[ -z "$VIRTUAL_ENV" ] && sudo apt install ansible -y
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
```

Install dependencies (Rocky Linux 8):
```bash
sudo yum install epel-release git -y
[ -z "$VIRTUAL_ENV" ] && sudo pip3 install ansible -y
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
```

**Install dependencies (Rocky Linux 9):**
```bash
sudo yum install epel-release git -y
[ -z "$VIRTUAL_ENV" ] && sudo yum install ansible -y
ansible-galaxy install collivier.xtesting
ansible-galaxy collection community.kubernetes
ansible-galaxy collection install -f community.docker
```

Install dependencies (Alpine 3.18):
```bash
sudo apk update && sudo apk add git
[ -z "$VIRTUAL_ENV" ] && sudo apk add ansible
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
ansible-galaxy collection install -f community.docker
```

Install dependencies (Alpine 3.19):
```bash
sudo apk update && sudo apk add git
[ -z "$VIRTUAL_ENV" ] && sudo apk add ansible
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
ansible-galaxy collection install -f community.docker
```

Install dependencies (Alpine 3.20):
```bash
sudo apk update && sudo apk add git
[ -z "$VIRTUAL_ENV" ] && sudo apk add ansible
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
ansible-galaxy collection install -f community.docker
```

**Install dependencies (Alpine 3.21):**
```bash
sudo apk update && sudo apk add git
[ -z "$VIRTUAL_ENV" ] && sudo apk add ansible
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
```

Install dependencies (Alpine Edge):
```bash
sudo apk update && sudo apk add git
[ -z "$VIRTUAL_ENV" ] && sudo apk add ansible
ansible-galaxy install collivier.xtesting
ansible-galaxy collection install community.kubernetes
ansible-galaxy collection install -f community.docker
```

## If proxy

All Xtesting CI playbooks could be executed behind a proxy and the proxy
settings would be copied in docker daemon configuration files. You can set the
remote environment at the play level.

Here is the configuration used in the gates
```bash
diff --git a/ansible/site.yml b/ansible/site.yml
index ed71e7c3..612b65bc 100644
--- a/ansible/site.yml
+++ b/ansible/site.yml
@@ -14,3 +14,7 @@
         - container: xtesting-mts
           tests:
             - seventh
+  environment:
+    http_proxy: 'http://admin:admin@{{ ansible_default_ipv4.address }}:3128'
+    https_proxy: 'http://admin:admin@{{ ansible_default_ipv4.address }}:3128'
+    no_proxy: '{{ ansible_default_ipv4.address }}'
```

## Deploy your Xtesting CI/CD toolchain (Jenkins)

Deploy your own Xtesting toolchain
```bash
git clone https://gerrit.opnfv.org/gerrit/functest-xtesting functest-xtesting-src
ansible-playbook functest-xtesting-src/ansible/site.yml
```

Access to the different dashboards:
- Jenkins: http://127.0.0.1:8080/ (admin/admin)
- Minio: http://127.0.0.1:9000/ (xtesting/xtesting)
- S3www: http://127.0.0.1:8181/
- TestAPI: http://127.0.0.1:8000

## Deploy your Xtesting CI/CD toolchain (GitLab CI/CD)

Deploy your own Xtesting toolchain
```bash
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
       builds:
         dependencies:
           - repo: _
EOF
popd
ansible-playbook functest-xtesting-src/ansible/site.yml
```

Access to the different dashboards:
- GitLab: http://127.0.0.1/ (xtesting/xtesting)
- Minio: http://127.0.0.1:9000/ (xtesting/xtesting)
- S3www: http://127.0.0.1:8181/
- TestAPI: http://127.0.0.1:8000

## Deploy your Functest CI/CD toolchain

Deploy your own Functest toolchain
```bash
git clone https://gerrit.opnfv.org/gerrit/functest functest-src
ansible-playbook functest-src/ansible/site.yml
```

Note: By default, the latest version is considered, if you want to create a
gate for a specific Functest version (i.e. a specific OpenStack version), you
can checkout the right branch.

Deploy your own Functest Hunter toolchain
```bash
git clone https://gerrit.opnfv.org/gerrit/functest functest-src
(cd functest-src && git checkout -b stable/hunter origin/stable/hunter)
ansible-playbook functest-src/ansible/site.yml
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

Deploy your own CNTT Nile toolchain
```bash
git clone https://gerrit.opnfv.org/gerrit/functest functest-src
ansible-playbook functest-src/ansible/site.cntt.yml
```

Note: By default, CNTT Nile is considered, if you want to create a gate for a
specific CNTT version, you can checkout the right branch.

Deploy your own CNTT Kali toolchain
```bash
git clone https://gerrit.opnfv.org/gerrit/functest functest-src
(cd functest-src && git checkout -b stable/leguer origin/stable/leguer)
ansible-playbook functest-src/ansible/site.cntt.yml
```

As a reminder the version table can be summarized as follows:

| Functest releases | OpenStack releases |CNTT releases  |
|-------------------|--------------------|---------------|
| Jerma             | Train              | Kali          |
| Kali              | Ussuri             | Kali          |
| Leguer            | Victoria           | Kali          |
| Wallaby           | Wallaby            | Nile          |
| Xena              | Xena               | Nile          |
| Yoga              | Yoga               | Nile          |
| Master            | next Antelope      | Nile          |

Here are the default Functest tree as proposed in Run Alpine Functest
containers (master):
- /home/opnfv/functest/openstack.creds
- /home/opnfv/functest/images


## Deploy your Functest Kubernetes CI/CD toolchain

Deploy your own Functest toolchain
```bash
git clone https://gerrit.opnfv.org/gerrit/functest-kubernetes functest-kubernetes-src
ansible-playbook functest-kubernetes-src/ansible/site.yml
```

Note: By default, the latest version is considered, if you want to create a
gate for a specific Functest version (i.e. a specific Kubernetes version), you
can checkout the right branch:

Deploy your own Functest Kubernetes Hunter toolchain
```bash
git clone https://gerrit.opnfv.org/gerrit/functest-kubernetes functest-kubernetes-src
(cd functest-kubernetes-src && git checkout -b stable/v1.32 origin/stable/v1.32)
ansible-playbook functest-kubernetes-src/ansible/site.yml
```

As a reminder the version table can be summarized as follows:

| Functest releases | Kubernetes releases |
|-------------------|---------------------|
| v1.29             | v1.29               |
| v1.30             | v1.30               |
| v1.31             | v1.31               |
| v1.32             | v1.32               |
| Master            | latest              |

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
FROM opnfv/xtesting:yoga

COPY hello.robot /home/opnfv/hello.robot
COPY testcases.yaml /etc/xtesting/testcases.yaml
```

Write testcases.yaml
```yaml
---
tiers:
  - name: hello
    testcases:
      - case_name: hello
        project_name: helloworld
        run:
          name: robotframework
          args:
            suites:
              - /home/opnfv/hello.robot
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
      registry_deploy: true
      repo: 127.0.0.1
      dport: 5000
      suites:
        - container: hello
          tests:
            - hello
```

Deploy your own Xtesting toolchain
```bash
ansible-playbook site.yml
```

```bash
PLAY RECAP ****************************************************************
127.0.0.1                  : ok=17   changed=11   unreachable=0    failed=0
```

Publish your container on your local registry
```bash
sudo docker push 127.0.0.1:5000/hello
```

## Deploy in production

### Encrypt your passwords

The default XtestingCI passwords are simple and clear text on purpose. But it
must be noted that XtestingCI allows overriding any password (via encryped
values or not). Here are basic instructions to encrypt XtestingCI content with
Ansible Vault. Please see
[Encrypting content with Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html#encrypting-content-with-ansible-vault)
for more details

Create a password file:
```bash
echo foo > a_password_file
```

Encrypt a new Jenkins password (here jenkins_password):
```bash
ansible-vault encrypt_string --vault-id a_password_file jenkins_password --name jenkins_password
```

Copy the encrypted password in site.yml
```yaml
---
- hosts: 127.0.0.1
  roles:
    - role: collivier.xtesting
      jenkins_password: !vault |
        $ANSIBLE_VAULT;1.1;AES256
        61656635613563666461306365383339313939613833366137353935643466633661633736313135
        3836393631336431646539663236313039396630623635650a653335363134343863383764343066
        63336464306632613563303032333534353565396666386561303061653332623266356462623461
        3633353764373737370a313564353536353263373663306630333565636132383932653436643266
        66373739393163366164626463366362613062353533643933633064656432343139
```

Deploy your own toolchain
```bash
ansible-playbook --vault-password-file a_password_file vault.yml
```

### Use verified Docker images

XtestingCI priorly selects the official images as proposed by the upstream
projects. Be free to use any custom image if it fits your security best
practices or any other enterprise choice. It's worth mentioning that all
specific XtestingCI Docker containers are built on a daily basis and verified
via Trivy to warn the endusers about any CVE known for the containerized
services or for the underlying distributions.

In the same manner, XtestingCI selects an official PostgreSQL container based
on Alpine. Here is a simple example picking another one based on Debian.
```yaml
---
- hosts: 127.0.0.1
  roles:
    - role: collivier.xtesting
      postgres_docker_tag: 13-bullseye
```

The following example switches from Gitlab Community Edition to
Gitlab Enterprise Edition:
```yaml
---
- hosts: 127.0.0.1
  roles:
    - role: collivier.xtesting
      jenkins_deploy: false
      gitlab_deploy: true
      gitlab_docker_image: gitlab/gitlab-ee
      gitlab_docker_tag: 13.12.11-ee.0
```

### Enable HTTPS

XtestingCI can deploy and configure NGINX as a reverse proxy to enable HTTPS
for Jenkins, S3www and TestAPI. The following example would ask XtestingCI to
generate a private key and self-signed certificate:
```yaml
---
- hosts: 127.0.0.1
  roles:
    - role: collivier.xtesting
      nginx_deploy: true
      http_dst_url: https://{{ external_ipaddress }}{{ nginx_s3_location }}
      testapi_ext_url: https://{{ external_ipaddress }}{{ nginx_testapi_location}}/api/v1
```

Be free to specify the server certificate and private key files as below :
```yaml
---
- hosts: 127.0.0.1
  roles:
    - role: collivier.xtesting
      nginx_deploy: true
      http_dst_url: https://{{ external_ipaddress }}{{ nginx_s3_location }}
      testapi_ext_url: https://{{ external_ipaddress }}{{ nginx_testapi_location}}/api/v1
      ssl_certificate: /tmp/foo.crt
      ssl_certificate_key: /tmp/foo.key
```

Access to the different dashboards:
- Jenkins: https://127.0.0.1 (admin/admin)
- S3www: https://127.0.0.1/s3
- TestAPI: https://127.0.0.1/testapi

### Tune your Continuous Integration toolchain

XtestingCI supports multiple deployment models such as all-in-one (in Docker or
in Kubernetes), centralized services (e.g. OPNFV toolchain) or a mix of both.

It follows [the KISS principle](https://en.wikipedia.org/wiki/KISS_principle),
by spliting all deployment and configuration steps and by leveraging urls for
any configuration action. The same operations can be applied whatever the
services are deployed via Docker, via Kubernetes or via any other way out of
XtestingCI.

XtestingCI defines lots of variables to finely select the services
(Jenkins vs GitLab, Minio vs Ceph radosgw, etc.) or the steps
you want to execute. For instance, *jenkins_deploy* decides if you install
Jenkins or not, *jenkins_configure* (in addition to *jenkins_url*) if you
configure it. The same model is generalized for all the services.

The default configuration setups the following services in a single host but
you're free to change it at your convenience; it's just about setting booleans
and urls:
- Jenkins
- MongoDB
- TestAPI
- Minio
- PostgreSQL
- Cachet

Please see the following Katacoda training courses which quickly highlight a
few distributed scenarios:
- [Distribute your Continuous Integration toolchain](https://github.com/collivier/katacoda-scenarios/tree/main/xtestingci/distributed)
- [Deploy the toolchain in your Kubernetes cluster](https://github.com/collivier/katacoda-scenarios/tree/main/xtestingci/cluster)

Note: Kubernetes allows defining Pod Security Policies in case the priviledged
test cases must be forbidden.
```yaml
---
- hosts: 127.0.0.1
  roles:
    - role: collivier.xtesting
      kubernetes_deploy: true
```

## Deploy your own CI/CD toolchain via the official virtual machine image

XtestingCI offers [diskimage-builder](https://docs.openstack.org/diskimage-builder/latest)'s
elements to build virtual machines ready for the CI/CD toolchain deployment.

These disk image files mostly contain the Ansible role and playbooks as
offered by XtestingCI but also all the container images needed for an offline
deployment.

Download the latest XtestingCI image:
```bash
wget https://artifacts.opnfv.org/xtestingci/xtestingci-latest.qcow2
```

Boot the virtual machine (Please fine tune the RAM size, CPUs and the tcp
ports according to the host capabilities)
```bash
sudo apt-get install qemu-system-x86 -y
sudo qemu-system-x86_64 -m 2048 -hda xtestingci-latest.qcow2 -nographic \
	-smp 4 -cpu host -accel kvm -device e1000,netdev=net0 \
	-netdev user,id=net0,hostfwd=tcp::10022-:22,hostfwd=tcp::8080-:8080,hostfwd=tcp::8181-:8181,hostfwd=tcp::8000-:8000
```

Connect as debian/debian to the virtual machine
```bash
ssh debian@localhost -p 10022
```

Download the official playbook running the Xtesting tescases by Jenkins and
then modify it to take both TestAPI and S3 redirections into consideration.
```bash
wget https://raw.githubusercontent.com/collivier/ansible-role-xtesting/master/tests/jenkins.yml
cat << EOF >> jenkins.yml
      testapi_ext_url: http://127.0.0.1:8000/api/v1
      http_dst_url: http://127.0.0.1:8181
EOF
```

(Optional) Pepare an offline deployment
```bash
tar -cC /data/docker/xtestingci . | sudo docker load
cat << EOF >> jenkins.yml
      offline: true
EOF
```

Deploy your own Xtesting toolchain
```bash
ansible-playbook jenkins.yml
```

Access to the different dashboards:
- Jenkins: http://127.0.0.1:8080 (admin/admin)
- S3www: http://127.0.0.1:8181
- TestAPI: http://127.0.0.1:8000

Please note also the following virtual machine images derivated from
the XtestingCI elements:
- Xtesting: https://artifacts.opnfv.org/xtesting/xtesting-latest.qcow2
- Functest: https://artifacts.opnfv.org/functest/functest-latest.qcow2
- Functest Kubernetes: https://artifacts.opnfv.org/functest-kubernetes/functest-kubernetes-latest.qcow2

## That's all folks!
