import setuptools

setuptools.setup(
    name="agentx",
    packages=setuptools.find_packages(exclude=["test"]),
    version="1.0.0",
    author="Tuan Nguyen Minh",
    author_email="tuana9a@gmail.com",
    entry_points={"console_scripts": ["agentx=agentx.cmd.daemon:main"]},
    install_requires=["python-dotenv==0.19.2"])
