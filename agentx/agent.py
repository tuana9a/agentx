import uuid
import crossplane

from typing import List
from agentx.configs import cfg
from agentx.models.crossplane import ParsedEntry
from typing import Optional, List
from agentx.configs import cfg as cfg
from agentx.utils.systemctl import SystemctlUtils
from agentx.models.nginx import ReverseProxyHTTP
from agentx.models.nginx import ReverseProxyHTTPS


def is_managed_config(n: str):
    return n.startswith("/etc/nginx/conf.d") or n == "/etc/nginx/nginx.conf"


class Agentx():
    id: Optional[str]
    conf_path: str
    configs: List[ParsedEntry]
    systemctl: SystemctlUtils

    def __init__(self, id: str, conf_path=cfg.default_nginx_config_path):
        self.id = id
        self.systemctl = SystemctlUtils("nginx")
        self.conf_path = conf_path
        self.configs = []
        for x in crossplane.parse(conf_path)["config"]:
            e = ParsedEntry(**x)
            if (is_managed_config(e.file)):
                self.configs.append(e)

    def add_reverse_proxy_http(self,
                               file: str,
                               server_name: str,
                               proxy_pass: str,
                               which_block: List[int] = [],
                               location="/",
                               port="80",
                               **kwargs):
        reverse_proxy = ReverseProxyHTTP(id=uuid.uuid4().hex,
                                         server_name=server_name,
                                         proxy_pass=proxy_pass,
                                         location=location,
                                         port=port)
        target_config: Optional[ParsedEntry] = None

        for conf in self.configs:
            if conf.file == file:
                target_config = conf
                break

        if not target_config:
            return

        target_blocks = target_config.parsed

        for i in which_block:
            directive_entry = target_blocks[i]
            if (not directive_entry):
                return
            target_blocks = directive_entry.block

        target_blocks.append(reverse_proxy.to_directive())

    def add_reverse_proxy_https(self,
                                file: str,
                                server_name: str,
                                proxy_pass: str,
                                ssl_certificate: str,
                                ssl_certificate_key: str,
                                which_block: List[int] = [],
                                location="/",
                                port="443",
                                **kwargs):
        reverse_proxy = ReverseProxyHTTPS(
            id=uuid.uuid4().hex,
            server_name=server_name,
            proxy_pass=proxy_pass,
            ssl_certificate=ssl_certificate,
            ssl_certificate_key=ssl_certificate_key,
            location=location,
            port=port)

        target_config: Optional[ParsedEntry] = None

        for conf in self.configs:
            if conf.file == file:
                target_config = conf
                break

        if not target_config:
            return

        target_blocks = target_config.parsed

        for i in which_block:
            directive_entry = target_blocks[i]
            if (not directive_entry):
                return
            target_blocks = directive_entry.block

        target_blocks.append(reverse_proxy.to_directive())

    def remove_conf(self,
                    file: str,
                    index: int,
                    which_block: List[int] = [],
                    **kwargs):
        target_config: Optional[ParsedEntry] = None

        for conf in self.configs:
            if conf.file == file:
                target_config = conf
                break

        if not target_config:
            return

        target_blocks = target_config.parsed

        for i in which_block:
            directive_entry = target_blocks[i]
            if (not directive_entry):
                return
            target_blocks = directive_entry.block

        target_blocks.pop(index)

    def get_current_configs_if_build(self, **kwargs):
        return list(
            map(lambda x: {
                "file": x.file,
                "build": x.build()
            }, self.configs))

    def reload(self, **kwargs):
        self.systemctl.reload()

    def save_config(self, file: str, **kwargs):
        for conf in self.configs:
            if conf.file == file:
                conf.save()
                return
