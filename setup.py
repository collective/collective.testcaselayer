from setuptools import setup, find_packages
import os

version = '1.6'

src_path = ("src", "collective", "testcaselayer")

tests_require = ['Plone']

setup(name='collective.testcaselayer',
      version=version,
      description="Use test cases as zope.testing layers",
      long_description='\n'.join(
          open(os.path.join(*path)).read() for path in [
              ("README.rst",),
              src_path + ("README.rst",),
              src_path + ("common.rst",),
              src_path + ("mail.rst",),
              src_path + ("ptc.rst",),
              src_path + ("ztc.rst",),
              src_path + ("layer.rst",),
              src_path + ("sandbox.rst",),
              src_path + ("functional.rst",),
              ("docs", "HISTORY.rst"),
              ("docs", "TODO.rst")
              ]),
      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
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
      package_dir={'': 'src'},
      include_package_data=True,
      namespace_packages=['collective'],
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'zope.testing>=3.6dev',
          'collective.monkeypatcher',
      ],
      tests_require=tests_require,
      extras_require={'tests': tests_require},
      entry_points="""
      # -*- Entry points: -*-
      """,
      test_suite="collective.testcaselayer.tests.test_suite",
      )
