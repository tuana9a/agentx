import multiprocessing

cpu_count = multiprocessing.cpu_count()
max_thread_pool_size = 8
min_thread_pool_size = 2
thread_pool_size = min(max(cpu_count, min_thread_pool_size),
                       max_thread_pool_size)

# bash
default_process_timeout_in_seconds = 30
interval_check_process_stopped_in_seconds = 5

# nginx
nginx_config_path = "/etc/nginx/nginx.conf"

# rabbitmq
transport_url: str = ""

# id
agentx_id: str = ""
