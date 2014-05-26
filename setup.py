__author__ = 'Nicholas C Pandolfi'

try:
    from setuptools import setup
except ImportError:
    from disutils.core import setup

description = '''
Offers two new dynamic types of file handles.
'''

long_description = '''
Reads randomly accessed lines from a text file faster than Python\'s built-in linecache,
and creates dynamic data types for the manipulation of massive data sets.
'''

githubpage = 'https://github.com/nickpandolfi/linereader'

setup(name='linereader',
      version='0.1.0',
      description=description,
      long_description=long_description,
      author='Nicholas C Pandolfi',
      author_email='viaanimi@gmail.com',
      url=githubpage,
      download_url=githubpage,
      license = 'The MIT License (MIT)',
      packages=['linereader'],
     )
