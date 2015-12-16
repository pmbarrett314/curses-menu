from setuptools import setup, find_packages
from setuptools.command import test as TestCommand
import sys


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
    name='curses-menu',
    version='1.0.0',
    url='',
    license='',
    author='Paul Barrett',
    author_email='',
    description='A simple console menu system using curses',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers'
    ],

    packages=find_packages(),
    # package_dir={'': 'cursesmenu'},

    setup_requires=['pytest-runner'],
    tests_require=['tox'],
    cmdclass={'test': Tox},

)
