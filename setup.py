#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='smallcalc',
    version='0.1.0',
    description="Small interpreter written in Python",
    long_description="",
    author="Leonardo Giordani",
    author_email='giordani.leonardo@gmail.com',
    url='https://github.com/lgiordani/smallcalc',
    packages=[
        'smallcalc',
    ],
    package_dir={'smallcalc':
                 'smallcalc'},
    include_package_data=True,
    install_requires=[],
    license="MIT license",
    zip_safe=False,
    keywords='smallcalc',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=[]
)
