from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='take_home',
    version='0.0.1',
    description='testing',
    author='Sebastian Gavilan',
    author_email='sebagavilan@gmail.com',
    url='https://github.com/sebaspower/take_home',
    # license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
