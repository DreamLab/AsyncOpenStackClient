import io
import re
from os.path import join, dirname, abspath
from setuptools import setup, find_packages


def read(name):
    here = abspath(dirname(__file__))
    return io.open(
        join(here, name), encoding='utf8'
    ).read()


setup(
    name="AsyncOpenStackClient",
    version="0.5.2",
    author='Dreamlab - PaaS KRK',
    author_email='paas-support@dreamlab.pl',
    url='https://github.com/DreamLab/AsyncOpenStackClient',
    description='Basic OpenStack client library using asyncio',
    long_description='%s\n%s' % (
        read('README.rst'),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=read('requirements.txt').split('\n'),
    zip_safe=False,
    keywords=[
        'iaas', 'cloud', 'openstack', 'nova', 'glance'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX',
        'Development Status :: 4 - Beta'
    ]
)
