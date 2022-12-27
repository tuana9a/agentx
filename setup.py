import setuptools

setuptools.setup(
    name="agentx",
    packages=setuptools.find_packages(exclude=["test"]),
    version="1.0.0",
    author="Tuan Nguyen Minh",
    author_email="tuana9a@gmail.com",
    entry_points={
        "console_scripts": [
            "agentx=agentx.cmd.daemon:main",
            "agentx-tools=agentx.cmd.tools:main"
        ]
    },
    install_requires=["crossplane>=0.5.8", "pydantic>=1.10.2", "pika>=1.3.1"])
