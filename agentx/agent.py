import uuid
import crossplane

from typing import Optional, List, Any
from agentx.models.crossplane import ParsedEntry
from agentx.models.crossplane import DirectiveEntry
from agentx.utils.systemctl import SystemctlUtils
from agentx.models.nginx import ReverseProxyHTTP
from agentx.models.nginx import ReverseProxyHTTPS


def is_managed_config(n: str):
    if n.startswith("/etc/nginx/conf.d"):
        return True
    if n.startswith("/etc/nginx/stream.conf.d"):
        return True
    if n == "/etc/nginx/nginx.conf":
        return True
    return False


class Agentx():
    id: Optional[str]
    conf_path: str
    configs: List[ParsedEntry]
    systemctl: SystemctlUtils

    def __init__(self, id: str, conf_path: str):
        self.id = id
        self.systemctl = SystemctlUtils("nginx")
        self.conf_path = conf_path
        self.configs = []
        self.reload_config()

    def add_reverse_proxy_http(self,
                               file: str,
                               server_name: str,
                               proxy_pass: str,
                               which_block: List[int] = [],
                               location="/",
                               port="80",
                               set_host_header=True,
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
            if (not directive_entry.block):
                return
            target_blocks = directive_entry.block

        target_blocks.append(reverse_proxy.to_directive(set_host_header))

    def add_reverse_proxy_https(self,
                                file: str,
                                server_name: str,
                                proxy_pass: str,
                                ssl_certificate: str,
                                ssl_certificate_key: str,
                                which_block: List[int] = [],
                                location="/",
                                port="443",
                                set_host_header=True,
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

        target_blocks: List[DirectiveEntry] = target_config.parsed

        for i in which_block:
            directive_entry = target_blocks[i]
            if (not directive_entry):
                return
            if (not directive_entry.block):
                return
            target_blocks = directive_entry.block

        target_blocks.append(reverse_proxy.to_directive(set_host_header))

    def remove_directive(self,
                         file: str,
                         which_block: List[int] = [],
                         **kwargs):
        target_config: Optional[ParsedEntry] = None

        for conf in self.configs:
            if conf.file == file:
                target_config = conf
                break

        if not target_config:
            return

        target_blocks: List[DirectiveEntry] = target_config.parsed

        last_index = which_block[len(which_block) - 1]
        which_block = which_block[0:(len(which_block) - 1)]

        for i in which_block:
            directive_entry = target_blocks[i]
            if (not directive_entry):
                return
            if (not directive_entry.block):
                return
            target_blocks = directive_entry.block

        target_blocks.pop(last_index)

    def update_directive(self,
                         file: str,
                         directive: str,
                         args: Optional[List[str]] = [],
                         block: Optional[List[DirectiveEntry]] = None,
                         which_block: List[int] = [],
                         **kwargs):
        target_config: Optional[ParsedEntry] = None

        for conf in self.configs:
            if conf.file == file:
                target_config = conf
                break

        if not target_config:
            return

        target_blocks: List[DirectiveEntry] = target_config.parsed

        last_index = which_block[len(which_block) - 1]
        which_block = which_block[0:(len(which_block) - 1)]

        for i in which_block:
            directive_entry = target_blocks[i]
            if (not directive_entry):
                return
            if (not directive_entry.block):
                return
            target_blocks = directive_entry.block

        target_blocks[last_index] = DirectiveEntry(directive=directive,
                                                   args=args,
                                                   block=block)

    def reload_server(self, **kwargs):
        self.systemctl.reload()

    def restart_server(self, **kwargs):
        self.systemctl.restart()

    def reload_config(self, **kwargs):
        self.configs = []
        for x in crossplane.parse(self.conf_path)["config"]:
            e = ParsedEntry(**x)
            if (is_managed_config(e.file)):
                self.configs.append(e)

    def save_config(self, file: str, **kwargs):
        for conf in self.configs:
            if conf.file == file:
                conf.save()
                return

    def save_config_then_reload_server(self, file: str, **kwargs):
        self.save_config(file)
        self.reload_server()
