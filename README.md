# agentx

Simple Nginx Agent run jobs

## how to setup (**python >= 3.8**)

**[NEW]** [agentx-tools](#agentx-tools) make setup simpler

config example see `agentx.ini.example`

prepare workspace folder

```bash
mkdir /opt/agentx
```

```bash
cd /opt/agentx
```

create new vitualenv

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

install package

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

```bash
sudo systemctl start agentx
```

(optional)

```bash
sudo systemctl enable agentx
```

## setup with `pip install -e .`

```bash
cd /opt
```

```bash
git clone https://github.com/tuana9a/agentx
```

```bash
cd /opt/agentx
```

create new vitualenv

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

install package

```bash
pip install -e .
```

## agentx-tools

gen config

```bash
agentx-tools gen config
```

install (ensure dirs, files + create config + create systemd service file)

keep your local version

```bash
agentx-tools install
```

reset install

reset all file (file, systemd service file)

```bash
agentx-tools install reset
```
