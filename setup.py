from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


setup(
    name='Mopidy-Cd-Autoplay',
    version=get_version('mopidy_cd_autoplay/__init__.py'),
    url='https://github.com/mczerski/mopidy-cd-autoplay',
    license='Apache License, Version 2.0',
    author='Marek Czerski',
    author_email='ma.czerski@gmail.com',
    description='Mopidy extension to automatically queue songs from audio CDs using Mopidy-Cd extension',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'pyudev >= 0.21.0',
        'Mopidy >= 2.0',
        'Pykka >= 1.1',
    ],
    entry_points={
        'mopidy.ext': [
            'cd_autoplay = mopidy_cd_autoplay:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
