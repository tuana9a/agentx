# agentx
Simple Nginx Agent run jobs

# how to setup (**python >= 3.8**)

```
mkdir /opt/agentx 
```

```
python3 -m venv .venv
```

```
source .venv/bin/activate
```

```bash
pip install git+https://github.com/tuana9a/agentx
```

create service file `/etc/systemd/system/agentx.service`

```ini
[Unit]
Description=Agentx Daemon

[Service]
ExecStart=/opt/agentx/.venv/bin/agentx --config /your/path/to/agentx.ini

[Install]
WantedBy=default.target
```

config example see `agentx.ini.example`
