import uuid

from typing import Union, List
from agentx.configs import cfg as cfg
from agentx.utils.systemctl_utils import SystemctlUtils
from agentx.utils.nginx_utils import ReverseProxyHTTP
from agentx.utils.nginx_utils import ReverseProxyHTTPS
from agentx.models.nginx_conf import NginxConf

nginx_systemctl = SystemctlUtils("nginx")
nginx_conf = NginxConf()


class Agent():

    def __init__(self):
        pass

    def add_nginx_reverse_proxy_http(self, **kwargs):
        conf = ReverseProxyHTTP(id=uuid.uuid4().hex, **kwargs)
        nginx_conf.add_conf(conf)

    def add_nginx_reverse_proxy_https(self, **kwargs):
        conf = ReverseProxyHTTPS(id=uuid.uuid4().hex, **kwargs)
        nginx_conf.add_conf(conf)

    def remove_conf(self, ids: List[int]):
        nginx_conf.remove_conf(ids)

    def get_current_nginx_conf(self):
        return nginx_conf.configs

    def reload_nginx(self):
        nginx_systemctl.reload()
