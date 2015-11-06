from setuptools import setup

setup(
    name='deflicker',
    version='0.1',
    description='adjust image brightness of images to get smooth timelapse',
    url='http://github.com/maxnoe/timelapse-deflicker',
    author='Maximilian Noethe',
    author_email='maximilian.noethe@tu-dortmund.de',
    license='MIT',
    packages=['deflicker', ],
    install_requires=[
        'numpy',
        'scikit-image',
        'progressbar2',
        'docopt',
        'schema',
    ],
    scripts=['scripts/timelapse-deflicker.py'],
    zip_safe=False,
)
