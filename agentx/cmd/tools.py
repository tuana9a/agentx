import uuid
import argparse

parser = argparse.ArgumentParser(prog="agentx-tools")

parser.add_argument("which",
                    help="Which module",
                    choices=["gen_config", "gen-config"],
                    type=str)

config_template = """
[default]
agentx_id={id}
nginx_config_path=/etc/nginx/nginx.conf
transport_url=amqps://username:password@rabbitmq.example.com/vhost
"""


def main():
    args = parser.parse_args()
    if args.which in ["gen_config", "gen-config"]:
        print(config_template.format(id=uuid.uuid4().hex))