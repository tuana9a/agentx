import time
import subprocess

from agentx.configs import cfg
from agentx.utils.thread_pool import default_thread_pool


def _kill_after_timeout(process: subprocess.Popen, timeout):
    max_count = int(timeout / cfg.interval_check_process_stopped_in_seconds)
    try:
        for i in range(max_count):
            time.sleep(cfg.interval_check_process_stopped_in_seconds)
            existed = process.poll()
            if existed is not None:
                # process return code
                return

        existed = process.poll()
        if not existed:
            # process return None means it's not return code yest (not stopped) so kill it
            process.kill()
            return
        # else do nothing
    except Exception as err:
        print(err)

    process.kill()


def run(cmd,
        timeout=cfg.default_process_timeout_in_seconds) -> subprocess.Popen:
    process = subprocess.Popen(cmd.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True)
    default_thread_pool.submit(_kill_after_timeout, process, timeout)
    return process
