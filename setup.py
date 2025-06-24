from setuptools import setup, find_packages

setup(
    name='network_tools',
    version='0.81',
    packages=find_packages(),
    install_requires=[
        'requests',
        'aiofiles',
    ],
)
