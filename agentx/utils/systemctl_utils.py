from agentx.utils.bash_utils import run


class SystemctlUtils():
    _service_name: str

    def __init__(self, service_name):
        self._service_name = service_name

    def start(self):
        service_name = self._service_name
        process = run(f"systemctl start {service_name}")
        stdout, stderr = process.communicate()
        return str(stdout + stderr).strip()

    def restart(self):
        service_name = self._service_name
        process = run(f"systemctl restart {service_name}")
        stdout, stderr = process.communicate()
        return str(stdout + stderr).strip()

    def reload(self):
        service_name = self._service_name
        process = run(f"systemctl reload {service_name}")
        stdout, stderr = process.communicate()
        return str(stdout + stderr).strip()

    def stop(self):
        service_name = self._service_name
        process = run(f"systemctl stop {service_name}")
        stdout, stderr = process.communicate()
        return str(stdout + stderr).strip()

    def enable(self):
        service_name = self._service_name
        process = run(f"systemctl enable {service_name}")
        stdout, stderr = process.communicate()
        return str(stdout + stderr).strip()

    def disable(self):
        service_name = self._service_name
        process = run(f"systemctl disable {service_name}")
        stdout, stderr = process.communicate()
        return str(stdout + stderr).strip()
