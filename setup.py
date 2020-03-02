import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def get_version():
    import pydns_cli
    return pydns_cli.__version__


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='mmt-server',
    version=get_version(),
    description='Base git repo for aggregating all services',
    long_description=readme(),
    classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    ],
    keywords='',
    url='http://github.com/',
    author='Jin Nguyen',
    author_email='dangtrinhnt@mymusictaste.com',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'Click',
        'colorama',
        'cookiecutter',
    ],
    setup_requires=[] + pytest_runner,
    tests_require=['pytest', 'pytest-asyncio', 'pytest-cov', 'pytest-redis'],
    entry_points='''
        [console_scripts]
        pydns=pydns.cli:
    ''',
    cmdclass={},
    zip_safe=False
)
