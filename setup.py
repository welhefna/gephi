from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='gephi',
    version='0.0.1',
    description='Gephi graph formats',
    long_description=readme,
    author='Wessam Elhefnawy',
    author_email='welhe001@odu.edu',
    url='https://github.com/kennethreitz/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

