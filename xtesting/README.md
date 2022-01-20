# Deploy your CI/CD toolchain as a Xtesting test case

```
sudo docker build -t xtestingci .
```

```
cat << EOF > hosts
xtestingci ansible_host=$(ip route get 1.1.1.1 | grep -oP 'src \K\S+') ansible_connection=ssh ansible_user=$(whoami) ansible_python_interpreter=/usr/bin/python3 ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOF
```

```
sudo docker run \
  -v ~/.ssh/id_rsa:/root/.ssh/id_rsa \
  -v $(pwd)/hosts:/src/inventory/hosts xtestingci
```
