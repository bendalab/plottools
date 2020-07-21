from setuptools import setup, find_packages

exec(open('plottools/version.py').read())

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='plottools',
    version=__version__,
    author='Jan Benda',
    author_email="jan.benda@uni-tuebingen.de",
    description='Simplify production of publication-quality figures based on matplotlib.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bendalab/plottools",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['numpy', 'matplotlib']
)
