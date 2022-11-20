from typing import List
from agentx.configs import cfg
from agentx.utils.nginx_utils import parse_conf


class NginxConf():

    def __init__(self) -> None:
        self.conf_path = cfg.default_nginx_config_path
        self.configs = []
        with open(self.conf_path, "r", encoding="utf-8") as f:
            conf = f.read()
            self.configs = parse_conf(conf)
        pass

    def add_conf(self, conf):
        self.configs.append(conf)
        with open(self.conf_path, "a", encoding="utf-8") as f:
            f.write(str(conf))

    def remove_conf(self, ids: List[int]):
        for id in ids:
            self.configs.pop(id)
        self.save()

    def save(self):
        with open(self.conf_path, "w", encoding="utf-8") as f:
            f.write("\n".join(list(map(lambda x: str(x), self.configs))))