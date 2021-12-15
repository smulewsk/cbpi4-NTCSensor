from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cbpi4-NTCSensor',
      version='0.0.1',
      description='CraftBeerPi4 NTC Sensor Plugin',
      author='Sebastian Mulewski',
      author_email='smulewsk@gmail.com',
      url='https://github.com/smulewsk/cbpi4-NTCSensor',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-NTCSensor': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-NTCSensor'],
      install_requires=[
            'cbpi>=4.0.0.33',
      ],
      long_description=long_description,
      long_description_content_type='text/markdown'
     )
