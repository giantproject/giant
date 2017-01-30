from setuptools import setup

setup(name='giant_repl',
      version='0.1',
      py_modules=['repl'],
      install_requires=['Click', 'requests', 'python-whois'],
      entry_points='''
      [console_scripts]
      repl=repl:cli'''
      )
