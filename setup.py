#!/usr/bin/env python

from distutils.core import setup
import pydevtools


with open('requirements.txt', 'r') as req_f:
    REQUIREMENTS = req_f.readlines()


setup(
    name='pydevtools',
    version=pydevtools.__version__,
    description='An assortment of python devtools',
    author=pydevtools.__author__,
    author_email='dev@kano.me',
    maintainer=pydevtools.__maintainer__,
    maintainer_email=pydevtools.__email__,
    url='https://github.com/KanoComputing/pydevtools',
    packages=[
        'pydevtools'
    ],
    license=pydevtools.__license__,
    install_requires=REQUIREMENTS
)
