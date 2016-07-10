# -*- coding: utf-8 -*-

from setuptools import setup

VERSION = '0.1.1'

setup(
    name='django-compoundqueryset',
    packages=[
        'djcompoundqueryset',
    ],
    version=VERSION,
    description='Allows for creation of compound querysets in Django.',
    url='https://github.com/brianwawok/django-compoundqueryset',
    download_url='https://github.com/brianwawok/django-compoundqueryset/' + VERSION,
    maintainer='Brian Wawok',
    maintainer_email='bwawok@gmail.com',
    install_requires=[
        'setuptools',
        'Django >= 1.8',
    ],
    platforms=['Any'],
    keywords=['django', 'compound', 'queryset'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Django',
    ],
)
