import io
import re
from setuptools import setup, find_packages
from os.path import join, dirname, abspath


def read(name):
    here = abspath(dirname(__file__))
    return io.open(
        join(here, name), encoding='utf8'
    ).read()


setup(
    name="AsyncOpenStackClient",
    version="0.1.1",
    author='Dreamlab - PaaS KRK',
    author_email='paas-support@dreamlab.pl',
    url='https://github.com/DreamLab/AsyncOpenStackClient',
    description='Basic OpenStack client library using asyncio',
    long_description='%s\n%s' % (
        read('README.md'),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.md'))
    ),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=read('requirements.txt').split('\n'),
    zip_safe=False,
    keywords=[
        'iaas', 'cloud',
        'openstack', 'nova',
    ],
    dependency_links=['https://pypi.python.org/pypi'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX',
        'Development Status :: 4 - Beta'
    ]
)
