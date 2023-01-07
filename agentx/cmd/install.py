import os
import sys
import uuid
import argparse

nginx_conf_path = "/etc/nginx/nginx.conf"
conf_d_path = "/etc/nginx/conf.d"
conf_d_agentx_path = "/etc/nginx/conf.d/agentx.conf"
stream_conf_d_path = "/etc/nginx/stream.conf.d"
stream_conf_d_agentx_path = "/etc/nginx/stream.conf.d/agentx.conf"
agentx_service_path = "/etc/systemd/system/agentx.service"
agentx_ini_template = """[default]
agentx_id={id}
nginx_config_path=/etc/nginx/nginx.conf
transport_url=
"""
agentx_service_template = """[Unit]
Description=Agentx Daemon

[Service]
ExecStart={exec_start} --config {config_path}

[Install]
WantedBy=default.target
"""
nginx_conf = """user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
  worker_connections 768;
  # multi_accept on;
}

http {
  sendfile on;
  tcp_nopush on;
  tcp_nodelay on;
  keepalive_timeout 65;
  types_hash_max_size 2048;
  # server_tokens off;

  server_names_hash_bucket_size 128;
  # server_name_in_redirect off;

  include /etc/nginx/mime.types;
  default_type application/octet-stream;

  ##
  # SSL Settings
  ##

  ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
  ssl_prefer_server_ciphers on;

  ##
  # Logging Settings
  ##

  access_log /var/log/nginx/access.log;
  error_log /var/log/nginx/error.log;

  ##
  # Gzip Settings
  ##

  gzip on;

  # gzip_vary on;
  # gzip_proxied any;
  # gzip_comp_level 6;
  # gzip_buffers 16 8k;
  # gzip_http_version 1.1;
  # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

  ##
  # Virtual Host Configs
  ##

  include /etc/nginx/conf.d/*.conf;
  include /etc/nginx/sites-enabled/*;
}

# agentx
stream {
  include /etc/nginx/stream.conf.d/*.conf;
}
"""

parser = argparse.ArgumentParser(prog="agentx-tools install")

parser.add_argument("--reset",
                    help="Reset installation",
                    required=False,
                    type=bool,
                    default=False,
                    const=True,
                    nargs="?")


def run(parent_args: argparse.Namespace):
    args = parser.parse_args(parent_args.remains)
    # /etc/nginx/conf.d/
    if not os.path.exists(conf_d_path):
        os.makedirs(conf_d_path)

    # /etc/nginx/stream.conf.d/
    if not os.path.exists(stream_conf_d_path):
        os.makedirs(stream_conf_d_path)

    # /etc/nginx/nginx.conf
    if args.reset:
        with open(nginx_conf_path, "w") as f:
            f.write(nginx_conf)

    # /etc/nginx/conf.d/agentx.conf
    if not os.path.exists(conf_d_agentx_path):
        with open(conf_d_agentx_path, "w") as f:
            f.write("")
    elif args.reset:
        with open(conf_d_agentx_path, "w") as f:
            f.write("")

    # /etc/nginx/stream.conf.d/agentx.conf
    if not os.path.exists(stream_conf_d_agentx_path):
        with open(stream_conf_d_agentx_path, "w") as f:
            f.write("")
    elif args.reset:
        with open(stream_conf_d_agentx_path, "w") as f:
            f.write("")

    # ./agentx.ini
    cwd = os.getcwd()
    config_path = cwd + "/agentx.ini"
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            f.write(agentx_ini_template.format(id=uuid.uuid4().hex))

    # agentx.service
    exec_path = sys.executable.split("/")
    exec_path[-1] = "agentx"
    exec_path = "/".join(exec_path)
    if not os.path.exists(agentx_service_path):
        with open(agentx_service_path, "w") as f:
            content = agentx_service_template.format(exec_start=exec_path,
                                                     config_path=config_path)
            f.write(content)
    elif args.reset:
        with open(agentx_service_path, "w") as f:
            content = agentx_service_template.format(exec_start=exec_path,
                                                     config_path=config_path)
            f.write(content)