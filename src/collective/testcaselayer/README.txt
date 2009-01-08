========================
collective.testcaselayer
========================

The support for layers provided by zope.testing helps to lessen the
amount of time consumed during test driven development by sharing
expensive test fixtures, such as is often requires for functional
test.  This package provides several well tested facilities to make
writing and using layers faster and easier.

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
