import pika
import json

from agentx.agent import Agentx
from agentx.configs import cfg
from agentx.configs import exchange_name


def main():
    agentx = Agentx(cfg.agentx_id)

    def callback(ch, method, properties, body):
        try:
            print(" [x] Received %r" % body)
            payload = json.loads(body)
            action = getattr(agentx, payload["method"])
            action(**payload)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(e)

    conn = pika.BlockingConnection(pika.URLParameters(cfg.transport_url))
    channel = conn.channel()
    channel.basic_qos(prefetch_count=1)

    agentx_qname = f"agentx-{cfg.agentx_id}"

    channel.queue_declare(agentx_qname)
    channel.exchange_declare(exchange_name.control_signal,
                             exchange_type="direct")

    channel.queue_bind(agentx_qname, exchange_name.control_signal,
                       cfg.agentx_id)
    channel.basic_consume(agentx_qname,
                          on_message_callback=callback,
                          auto_ack=False)

    print(' [*] Waiting for control. To exit press CTRL+C')
    channel.start_consuming()