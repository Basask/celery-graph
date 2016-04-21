# -*- coding: utf-8 -*-
# @Date    : 2016-04-21 09:55:24
# @Author  : Rafael Fernandes (basask@collabo.com.br)
# @Link    : http://www.collabo.com.br/

import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='celery_graph',
    version='0.0.1',
    description='Builds celery tasks from an IGraph graph',
    long_description=README,
    url='https://github.com/Basask/celery-graph',
    author='Basask',
    author_email='basask@collabo.com.br',
    include_package_data=True,
    license='MIT License',
    packages=[
        'celery_graph'
    ],
    install_requires=[
        'celery',
        'python-igraph'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
)
