import os
import re
import sys
import glob
import codecs

from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand


here = os.path.abspath(os.path.dirname(__file__))

setup_requires = ['pytest']
install_requires = ['flask', 'prettyconf']
dev_requires = ['pyflakes', 'pep8', 'pylint', 'check-manifest',
                'ipython', 'ipdb', 'sphinx', 'sphinx_rtd_theme',
                'sphinxcontrib-napoleon', 'wheel', 'twine']
tests_require = ['pytest-cov', 'pytest-cache', 'pytest-timeout',
                 'pytest-asyncio==0.2.0', 'tox']
dev_requires.append(tests_require)

version = "0.0.0"
changes = os.path.join(here, "CHANGES.md")
match = '^#*\s*(?P<version>[0-9]+\.[0-9]+(\.[0-9]+)?)$'
with codecs.open(changes, encoding='utf-8') as changes:
    for line in changes:
        match = re.match(match, line)
        if match:
            version = match.group("version")
            break

# Get the long description
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get version
with codecs.open(os.path.join(here, 'CHANGES.md'), encoding='utf-8') as f:
    changelog = f.read()


class VersionCommand(Command):
    description = "print library version"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long',
                          '--cov', 'echod', '--cov-report',
                          'term-missing', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


setup(
    name='curytybainbox',
    version='0.1.0',
    description='Curytyba in a box in a clone of tempoescope using Python and Intel Edison',
    long_description=long_description,
    url='https://github.com/wiliamsouza/echod',
    author='The curytybainbox Authors',
    author_email='garagemhaker0@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: No Input/Output (Daemon)',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Testing'
    ],
    keywords='python edison curytyba',
    packages=find_packages(exclude=['docs', 'tests*']),
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'dev': dev_requires,
        'test': tests_require,
    },
    data_files=[
        ('/lib/systemd/system/', glob.glob('systemd/*.service')),
        ('/etc/curytybainbox/', glob.glob('environment')),
    ],
    cmdclass={
        "version": VersionCommand,
        'test': PyTest,
        "tox": Tox,
    },
    entry_points={
        'console_scripts': [
            'curytybainboxd = curytybainbox.curytybainboxd:main',
            'curytybainboxweb = curytybainbox.curytybainboxweb:main',
        ]
    },
)
