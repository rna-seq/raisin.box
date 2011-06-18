from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(name='rnaseq.box',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      namespace_packages = ['rnaseq'],
      package_data = {'rnaseq.box':['*.ini']},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'configobj',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
