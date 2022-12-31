# agentx

Simple Nginx Agent run jobs

## how to setup (**python >= 3.8**)

config example see `agentx.ini.example`

```bash
mkdir /opt/agentx
```

```bash
cd /opt/agentx
```

```bash
python3 -m venv .venv
```

```bash
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
ExecStart=/opt/agentx/.venv/bin/agentx --config /opt/agentx/agentx.ini

[Install]
WantedBy=default.target
```

```bash
sudo systemctl daemon-reload
```

(optional)

```bash
sudo systemctl enable agentx
```
