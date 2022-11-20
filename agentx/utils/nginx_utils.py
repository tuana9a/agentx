from agentx.configs import cfg


class ConfigEntry():

    def __init__(self, id, lines=[]) -> None:
        self.id = id
        self.lines = lines
        pass

    def __str__(self) -> str:
        return "\n".join(self.lines)


class ReverseProxyHTTP(ConfigEntry):

    def __init__(self,
                 id: str,
                 server_name: str,
                 proxy_pass: str,
                 location="/",
                 port="80",
                 **kwargs):
        ConfigEntry.__init__(self, id=id)
        self.server_name = server_name
        self.proxy_pass = proxy_pass
        self.location = location
        self.port = port
        self.lines = [
            cfg.agentx_config_notation + self.id,
            "server {",
            "  listen " + str(self.port) + ";",
            "  server_name " + self.server_name + ";",
            "  location " + self.location + " {",
            "    proxy_pass " + self.proxy_pass + ";",
            "  }",
            "}",
        ]


class ReverseProxyHTTPS(ConfigEntry):

    def __init__(self,
                 id: str,
                 server_name: str,
                 proxy_pass: str,
                 ssl_certificate: str,
                 ssl_certificate_key: str,
                 location="/",
                 port="443",
                 **kwargs):
        ConfigEntry.__init__(self, id=id)
        self.server_name = server_name
        self.proxy_pass = proxy_pass
        self.location = location
        self.port = port
        self.ssl_certificate = ssl_certificate
        self.ssl_certificate_key = ssl_certificate_key
        self.lines = [
            cfg.agentx_config_notation + self.id,
            "server {",
            "  listen " + str(self.port) + " ssl;",
            "  ssl_certificate" + self.ssl_certificate + ";",
            "  ssl_certificate_key " + self.ssl_certificate_key + ";",
            "  server_name " + self.server_name + ";",
            "  location " + self.location + " {",
            "    proxy_pass " + self.proxy_pass + ";",
            "  }",
            "}",
        ]


def parse_conf(conf: str):
    configs = []
    stack = []
    current_line_idx = -1
    current_conf_start = 0
    current_conf_id = ""
    prefix_notation = cfg.agentx_config_notation

    lines = conf.split("\n")
    for line in lines:
        current_line_idx += 1

        if line.startswith(prefix_notation):
            current_conf_start = current_line_idx + 1
            current_conf_id = line[len(prefix_notation):]
        else:
            for char in line:
                if char == "{":
                    stack.append(char)
                elif char == "}":
                    stack.pop()
                    if len(stack) == 0:
                        start_idx = current_conf_start
                        end_idx = current_line_idx + 1
                        entry = ConfigEntry(current_conf_id,
                                            lines=lines[start_idx:end_idx])
                        configs.append(entry)

    return configs
