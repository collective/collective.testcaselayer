from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.testcaselayer',
      version=version,
      description="Use test case classes as zope.testing layers",
      long_description='\n'.join(
          open(os.path.join(*path)).read() for path in [
              ("collective", "testcaselayer", "README.txt"),
              ("collective", "testcaselayer", "ptc.txt"),
              ("collective", "testcaselayer", "ztc.txt"),
              ("collective", "testcaselayer", "layer.txt"),
              ("collective", "testcaselayer", "sandbox.txt"),
              ("docs", "HISTORY.txt"),
              ("docs", "TODO.txt")
              ]),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ross Patterson',
      author_email='me@rpatterson.net',
      url='http://pypi.python.org/pypi/collective.testcaselayer',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'zope.testing',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      test_suite = "collective.testcaselayer.tests.test_suite",
      )
