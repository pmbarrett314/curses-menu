from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys
import re


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
        license='',
        author='Paul Barrett',
        author_email='pmbarrett314@gmail.com',
        description='A simple console menu system using curses',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python :: 3.5',
            'Intended Audience :: Developers'
        ],

        packages=find_packages(),
        setup_requires=['pytest-runner'],
        tests_require=['tox'],
        cmdclass={'test': Tox},

)
