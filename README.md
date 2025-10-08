## exp-sync
Tool designed for the pwncollege environment, where the main vulnerable machine is landlocked and can only be accessed through ssh.

## Installation
```bash
git clone https://github.com/fexsecc/exp-sync.git /opt/exp-sync
sudo ln -s /opt/exp-sync/exp-sync.py /usr/local/bin/exp-sync.py
```

## Usage
```bash
exp-sync.py -h
exp-sync.py -f <FILE> &
nohup exp-sync.py -f <FILE> >/dev/null 2>&1 &
```
