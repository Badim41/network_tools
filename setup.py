from setuptools import setup, find_packages

setup(
    name='network_tools',
    version='3.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'aiofiles',
        'aiohttp'
    ],
)
