"""Setuptools for eleanor_client"""
from setuptools import setup, find_packages

reqs = []

with open('requirements.txt') as inf:
    for line in inf:
        line = line.strip()
        reqs.append(line)


setup(
    name='eleanor-client',
    version='0.3',
    description='Package for interacting with eleanor service',
    author='Brett Smythe',
    author_email='smythebrett@gmail.com',
    maintainer='Brett Smythe',
    maintainer_email='smythebrett@gmail.com',
    packages=find_packages(),
    install_reqs=reqs
)
