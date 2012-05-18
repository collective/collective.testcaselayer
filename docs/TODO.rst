TODO
====

* Add convenience method for loading ZCML. (witsch)

* Factor out collective.testclasslayer.layer

The collective.testclasslayer.layer module doesn't actually have
anything to do with test cases, but I didn't want to create a separate
package just for this one bit.  If someone wants to put this in
zope.testing or some other common testing dependency, that would be
great.

* Factor unittest.TestCase out of Testing.ZopeTestCase.base.TestCase

It might be appropriate to refactor out the ZTC specific pieces of the
test cases in the Testing.ZopeTestCase package such that there is a
common base class that doesn't subclass unittest.TestCase.  With this
in place we could do away with collective.testcaselayer.testcase and
have common base classes that could be used either as layers or as
test cases.
