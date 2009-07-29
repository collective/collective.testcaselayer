from setuptools import setup, find_packages
import os

version = '1.0'

src_path = ("src", "collective", "testcaselayer")

setup(name='collective.testcaselayer',
      version=version,
      description="Use test cases as zope.testing layers",
      long_description='\n'.join(
          open(os.path.join(*path)).read() for path in [
              src_path + ("README.txt",),
              src_path + ("ptc.txt",),
              src_path + ("ztc.txt",),
              src_path + ("layer.txt",),
              src_path + ("sandbox.txt",),
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
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir = {'':'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'zope.testing>=3.6dev',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      test_suite="collective.testcaselayer.tests.test_suite",
      )
