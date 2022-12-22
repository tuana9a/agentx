import os
import sys
import pika
import json
import time
import traceback
import logging
import argparse
import configparser

from agentx.agent import Agentx
from agentx.configs import cfg
from agentx.configs import exchange_name
from agentx.utils.thread import default_thread_pool

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)

parser = argparse.ArgumentParser(prog="agentx")

parser.add_argument("-c",
                    "--config",
                    help="Agentx config path",
                    required=True,
                    type=str)


def main():
    args = parser.parse_args()
    config_parser = configparser.ConfigParser()
    config_parser.read(args.config)

    for section in config_parser.sections():
        cfg.agentx_id = config_parser[section]["agentx_id"]
        cfg.nginx_config_path = config_parser[section]["nginx_config_path"]
        cfg.transport_url = config_parser[section]["transport_url"]

    agentx = Agentx(cfg.agentx_id, cfg.nginx_config_path)
    logging.info(f'agentx_id {cfg.agentx_id}')

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
