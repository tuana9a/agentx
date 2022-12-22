import os
import sys
import pika
import json
import time
import traceback
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)

from agentx.agent import Agentx
from agentx.configs import cfg
from agentx.configs import exchange_name
from agentx.utils.thread import default_thread_pool


def main():
    agentx = Agentx(cfg.agentx_id)

    def callback(ch, method, properties, body):
        try:
            logging.info(" [x] Received %r" % body)
            payload = json.loads(body)
            action = getattr(agentx, payload["method"])
            action(**payload)
        except Exception as e:
            logging.error(traceback.format_exc())

        ch.basic_ack(delivery_tag=method.delivery_tag)

    stop = False

    def send_current_configs():
        conn = pika.BlockingConnection(pika.URLParameters(cfg.transport_url))
        channel = conn.channel()
        channel.exchange_declare(exchange_name.current_configs,
                                 exchange_type="fanout")
        try:
            while not stop:
                payload = {
                    "agentx_id": cfg.agentx_id,
                    "configs": list(map(lambda x: x.dict(), agentx.configs))
                }
                channel.basic_publish(exchange=exchange_name.current_configs,
                                      routing_key="",
                                      body=json.dumps(payload))
                time.sleep(3)
        except Exception as e:
            logging.error(traceback.format_exc())

    def send_current_configs_if_build():
        conn = pika.BlockingConnection(pika.URLParameters(cfg.transport_url))
        channel = conn.channel()
        channel.exchange_declare(exchange_name.current_configs_if_build,
                                 exchange_type="fanout")
        try:
            while not stop:
                payload = {
                    "agentx_id": cfg.agentx_id,
                    "configs": agentx.get_current_configs_if_build()
                }
                channel.basic_publish(
                    exchange=exchange_name.current_configs_if_build,
                    routing_key="",
                    body=json.dumps(payload))
                time.sleep(3)
        except Exception as e:
            logging.error(traceback.format_exc())

    default_thread_pool.submit(fn=send_current_configs)
    default_thread_pool.submit(fn=send_current_configs_if_build)

    try:
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
        logging.info(' [*] Waiting for control. To exit press CTRL+C')
        channel.start_consuming()

    except KeyboardInterrupt:
        stop = True
        logging.info('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
