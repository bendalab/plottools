from distutils.core import setup
from setuptools import find_packages

exec(open('plottools/version.py').read())

setup(name='plottools',
      version=__version__,
      packages=find_packages(exclude=['contrib', 'doc', 'tests*']),
      description='Simplify creation of publication-quality figures.',
      author='Jan Benda',
      requires=['numpy', 'matplotlib']
      )
