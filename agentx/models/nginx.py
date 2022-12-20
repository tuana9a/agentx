from typing import Optional
from pydantic import BaseModel
from agentx.models.crossplane import DirectiveEntry


class ReverseProxyHTTP(BaseModel):
    id: Optional[str] = None
    server_name: str
    proxy_pass: str
    location: str = "/"
    port: str = "80"

    def to_directive(self):
        return DirectiveEntry(
            directive="server",
            block=[
                DirectiveEntry(directive="listen", args=[str(self.port)]),
                DirectiveEntry(directive="server_name",
                               args=[self.server_name]),
                DirectiveEntry(directive="location",
                               args=[self.location],
                               block=[
                                   DirectiveEntry(directive="proxy_pass",
                                                  args=[self.proxy_pass])
                               ]),
            ])


class ReverseProxyHTTPS(BaseModel):
    id: Optional[str] = None
    server_name: str
    proxy_pass: str
    ssl_certificate: str
    ssl_certificate_key: str
    location: str = "/"
    port: str = "443"

    def to_directive(self):
        return DirectiveEntry(
            directive="server",
            block=[
                DirectiveEntry(directive="listen",
                               args=[str(self.port), "ssl"]),
                DirectiveEntry(directive="server_name",
                               args=[self.server_name]),
                DirectiveEntry(directive="ssl_certificate",
                               args=[self.ssl_certificate]),
                DirectiveEntry(directive="ssl_certificate_key",
                               args=[self.ssl_certificate_key]),
                DirectiveEntry(directive="location",
                               args=[self.location],
                               block=[
                                   DirectiveEntry(directive="proxy_pass",
                                                  args=[self.proxy_pass])
                               ]),
            ])
