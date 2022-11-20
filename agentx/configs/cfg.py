import os
import multiprocessing
import dotenv

dotenv.load_dotenv()

cpu_count = multiprocessing.cpu_count()
max_thread_pool_size = 8
min_thread_pool_size = 2
default_thread_pool_size = min(max(cpu_count, 1), 8)

# bash
default_process_timeout_in_seconds = 30
interval_check_process_stopped_in_seconds = 5

# docker
default_stop_container_timeout_in_seconds = 3 * 60

# nginx
default_nginx_config_path = "/etc/nginx/conf.d/agentx.conf"
agentx_config_notation = "###agentx"
default_nginx_conf_delimiter = ";"
