from setuptools import setup, find_packages

setup(name = 'Greengraph',
      version = '0.1',
      description = 'Green space between London and Birmingham.',
      packages = find_packages(exclude=['test*']),
      install_requires = ['geopy', 'requests', 'pypng', 'numpy', 'matplotlib', 'url']
      #scripts = ['scripts/greengraph']
      )
      