from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys
import re
import io


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


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


version_file_name = "cursesmenu/version.py"
version_file_contents = open("cursesmenu/version.py", "rt").read()
version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
match = re.search(version_regex, version_file_contents, re.M)
if match:
    __version__ = match.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (version_file_name,))

setup(
    name='curses-menu',
    version=__version__,
    url='http://github.com/pmbarrett314/curses-menu',
    license='MIT',
    author='Paul Barrett',
    author_email='pmbarrett314@gmail.com',
    description='A simple console menu system using curses',
    long_description=read("README.rst", "CHANGELOG.rst"),
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
