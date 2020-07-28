#!/usr/bin/env python

from setuptools import setup, find_packages
PROJECT = 'icontext'
VERSION = '0.1'
DOWNLOAD_URL = 'https://github.com/stefan-wolfsheimer/icontext/tarball/master'

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(name=PROJECT,
      version=VERSION,
      description='iRODS context switcher',
      long_description=long_description,
      author='Stefan Wolfsheimer',
      author_email='stefan.wolfsheimer@gmail.com',
      url='https://github.com/stefan-wolfsheimer/icontext',
      download_url=DOWNLOAD_URL,
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Intended Audience :: Developers',
                   'Environment :: Console'],
      platforms=['Any'],
      scripts=[],
      provides=[],
      install_requires=['Click',
                        'python-irodsclient',
                        'python-editor'],
      namespace_packages=[],
      packages=find_packages(),
      include_package_data=True,
      package_data={'icontext': ['*.sh']},
      entry_points={
          'console_scripts': [
              'icontext = icontext.main:main'
          ]
      },
      zip_safe=False)
