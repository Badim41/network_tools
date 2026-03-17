from setuptools import setup, find_packages

setup(
    name='network_tools',
    version='2.2',
    packages=find_packages(),
    install_requires=[
        'requests',
        'aiofiles',
        'aiohttp'
    ],
)
