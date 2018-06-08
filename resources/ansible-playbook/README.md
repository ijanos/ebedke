Test ansible

```
ansible all -i HOST, -m ping  -u fedora -e 'ansible_python_interpreter=/usr/bin/python3'
```

Run the playbook
```
ansible-playbook site.yml -i HOST, -u fedora -e 'ansible_python_interpreter=/usr/bin/python3'
```