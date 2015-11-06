from setuptools import setup
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='deflicker',
    version='0.1.1',
    description='Adjust the brightness of images for smooth timelapse videos',
    long_description=long_description,
    url='http://github.com/maxnoe/timelapse-deflicker',
    author='Maximilian Noethe',
    author_email='maximilian.noethe@tu-dortmund.de',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='image timelapse',
    packages=['deflicker', ],
    install_requires=[
        'numpy',
        'scikit-image',
        'progressbar2',
        'docopt',
        'schema',
    ],
    entry_points={
        'console_scripts': [
            'deflicker = deflicker.__main__:main',
        ],
    },
)
