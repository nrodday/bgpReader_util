from setuptools import setup

setup(name='bgpReader_util',
      version='0.2',
      description='Utility functions',
      url='https://github.com/nrodday/bgpReader_util',
      author='Andreas Reuter, Nils Rodday',
      author_email='andreas.reuter@fu-berlin.de, nils.rodday@unibw.de',
      license='MIT',
      packages=['bgpReader_util'],
      zip_safe=False, install_requires=['pandas', 'requests'])
