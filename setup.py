from setuptools import setup, find_packages

setup(
    name='network_tools',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'aiofiles',
        'aiohttp==3.8.6'
    ],
)
