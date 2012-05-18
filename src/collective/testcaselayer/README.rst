.. -*-doctest-*-

Quick Start
===========

For a simple testing layer which installs a collective namespace
package into Zope and installs it's GenericSetup profile into the
PloneTestCase Plone site you can do the following.

Specify the testing dependency on collective.testcaselayer in the
egg's setup.py::

    from setuptools import setup, find_packages
    ...
    tests_require = ['collective.testcaselayer']
    ...
    setup(name='collective.foo',
          ...
          install_requires=[
              'setuptools',
              # -*- Extra requirements: -*-
          ],
          tests_require=tests_require,
          extras_require={'tests': tests_require},
          ...
          entry_points="""

Tell your buildout to include the testing dependencies.  This is only
necessary for deployments where you'll be running the tests.  As such,
you can leave this out of your production buildout configuration and
put it only in your buildout's development configuration::

    ...
    eggs +=
        collective.foo [tests]
    ...

Define the layer.  The layer can use all the same methods as a
PloneTestCase class, such as:

    - self.login(user_name)
    - self.loginAsPortalOwner()
    - self.addProduct(product)
    - self.addProfile(profile)

An additional, method is provided to load a ZCML file with ZCML debug
mode enabled:

    - self.loadZCML(file, package=package)

You could use a collective.foo.testing module like this:

    >>> from Products.PloneTestCase import ptc
    >>> 
    >>> from collective.testcaselayer import ptc as tcl_ptc
    >>> from collective.testcaselayer import common
    >>> 
    >>> class Layer(tcl_ptc.BasePTCLayer):
    ...     """Install collective.foo"""
    ... 
    ...     def afterSetUp(self):
    ...         ZopeTestCase.installPackage('collective.foo')
    ...         
    ...         from collective.foo import tests
    ...         self.loadZCML('testing.zcml', package=tests)
    ...         
    ...         self.addProfile('collective.foo:default')
    >>> 
    >>> layer = Layer([common.common_layer])

To use this layer in a README.txt doctest, you could use a
collective.foo.tests module like this:

    >>> import unittest
    >>> import doctest
    >>> 
    >>> from Testing import ZopeTestCase
    >>> from Products.PloneTestCase import ptc
    >>>
    >>> from collective.foo import testing
    >>> 
    >>> optionflags = (doctest.NORMALIZE_WHITESPACE|
    ...                doctest.ELLIPSIS|
    ...                doctest.REPORT_NDIFF)
    >>> 
    >>> def test_suite():
    ...     suite = ZopeTestCase.FunctionalDocFileSuite(
    ...         'README.txt',
    ...         optionflags=optionflags,
    ...         test_class=ptc.FunctionalTestCase)
    ...     suite.layer = testing.layer
    ...     return suite
    >>> 
    >>> if __name__ == '__main__':
    ...     unittest.main(defaultTest='test_suite')

Now write your README.txt doctest and your tests can be run with
something like::

    $ bin/instance test -s collective.foo

Detailed Documentation
======================

.. contents:: Table of Contents

Layer authors often end up reproducing the functionality provided by
their test case classes since the same functionality is needed to
perform layer set up or tear down.  The collective.testcaselayer.ztc,
collective.testcaselayer.ctc, and collective.testcaselayer.ptc modules
provide layer base classes that mix in the test case functionality from
ZopeTestCase, CMFTestCase, and PloneTestCase, respectively.  See the
collective.testcaselayer.ztc, and collective.testcaselayer.ptc
sections below (or ztc.txt and ptc.txt if reading this in the source)
for more details.  These layer base classes also include the layer
base class support from collective.testcaselayer.layer and the
sandboxed ZODB layer support from collective.testcaselayer.sandbox
described below.  Additionally, these modules allow for using the test
case fixtures as layers themselves.

While class objects can be used as layers, as opposed to instances of
classes, doing so means that it is not possible for a layer to
subclass another layer *just* to re-use functionality without also
depending on that layer being set up as well.  See the
collective.testcaselayer.layer section below (or layer.txt if reading
this in the source) for more details.

The DemoStorage included with the ZODB provides a way to "nest" ZODB
stores such that all writes will go to the DemoStorage while reads
will be taken from the base storage if not available from the
DemoStorage.  The collective.testcaselayer.sandbox module uses this
feature to associate a DemoStorage with each sandboxed layer to which
set up changes are committed and restore the base storage on tear
down.  Thus sibling layers that write to the ZODB can be isolated from
each other.  See the collective.testcaselayer.sandbox section below
(or sandbox.txt if reading this in the source) for more details.
