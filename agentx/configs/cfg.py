import multiprocessing
import configparser
import uuid

cpu_count = multiprocessing.cpu_count()
max_thread_pool_size = 8
min_thread_pool_size = 2
default_thread_pool_size = min(max(cpu_count, 1), 8)

# bash
default_process_timeout_in_seconds = 30
interval_check_process_stopped_in_seconds = 5

# nginx
default_nginx_config_path = "/etc/nginx/nginx.conf"
default_config_path = "agentx.ini"

nginx_config_path = default_nginx_config_path
config_path = default_config_path

# rabbitmq
transport_url: str = ""

# id
agentx_id: str

parser = configparser.ConfigParser()
parser.read(config_path)
for section in parser.sections():
    agentx_id = parser[section].get("agentx_id", uuid.uuid4().hex)
    nginx_config_path = parser[section].get("nginx_config_path",
                                            default_nginx_config_path)
    transport_url = parser[section]["transport_url"]
