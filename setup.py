# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
# VERSION INFORMATION
from pigeon import __version__


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()
setup(
    name='pigeon',
    version=__version__,
    description='The python based data generation program',
    long_description=readme,
    author='Eve Rogers',
    author_email='eve@doubledash.org',
    url='https://github.com/oxide-one/pigeon',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),

    install_requires=[
        "pyyaml",
        "argcomplete",
        "jinja2",
        "faker",
        "colorlog"
        ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['pigeon-run=pigeon.cli.run:run'],
    }
)
