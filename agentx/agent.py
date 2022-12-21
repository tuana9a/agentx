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


class Agentx():
    id: Optional[str]
    conf_path: str
    configs: List[ParsedEntry]
    systemctl: SystemctlUtils
    configs: List[ParsedEntry]

    def __init__(self, id: str, conf_path=cfg.default_nginx_config_path):
        data = crossplane.parse(conf_path)
        self.id = id
        self.systemctl = SystemctlUtils("nginx")
        self.conf_path = conf_path
        self.configs = list(map(lambda x: ParsedEntry(**x), data["config"]))

    def add_reverse_proxy_http(self,
                               file: str,
                               server_name: str,
                               proxy_pass: str,
                               location="/",
                               port="80",
                               **kwargs):
        reverse_proxy = ReverseProxyHTTP(id=uuid.uuid4().hex,
                                         server_name=server_name,
                                         proxy_pass=proxy_pass,
                                         location=location,
                                         port=port,
                                         **kwargs)
        for conf in self.configs:
            if conf.file == file:
                conf.parsed.append(reverse_proxy.to_directive())
                return

    def add_reverse_proxy_https(self,
                                file: str,
                                server_name: str,
                                proxy_pass: str,
                                ssl_certificate: str,
                                ssl_certificate_key: str,
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
            port=port,
            **kwargs)
        for conf in self.configs:
            if conf.file == file:
                conf.parsed.append(reverse_proxy.to_directive())
                return

    def remove_conf(self, file: str, index: int, **kwargs):
        for conf in self.configs:
            if conf.file == file:
                conf.parsed.pop(index)
                return

    def get_current_configs(self, **kwargs):
        return self.configs

    def reload(self, **kwargs):
        self.systemctl.reload()

    def save_config(self, file: str, **kwargs):
        for conf in self.configs:
            if conf.file == file:
                conf.save()
                return
