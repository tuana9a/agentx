import uuid
import argparse

agentx_ini_template = """[default]
agentx_id={id}
nginx_config_path=/etc/nginx/nginx.conf
transport_url=
"""

parser = argparse.ArgumentParser(prog="agentx-tools gen")

parser.add_argument("which", choices=["config"])


def run(parent_args: argparse.Namespace):
    args = parser.parse_args(parent_args.remains)
    if args.which == "config":
        print(agentx_ini_template.format(id=uuid.uuid4().hex), end="")
