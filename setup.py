from setuptools import setup, find_packages


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
    #package_dir={'': 'cursesmenu'},

    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

)
