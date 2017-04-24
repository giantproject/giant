from setuptools import setup

setup(name='giant_one',
      version='0.1',
      py_modules=['giant_one'],
      install_requires=['Click', 'requests', 'python-whois'],
      entry_points='''
      [console_scripts]
      giant_one=giant_one:cli'''
      )
