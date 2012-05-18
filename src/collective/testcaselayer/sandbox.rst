.. -*-doctest-*-

collective.testcaselayer.sandbox
================================

Sandboxed layers commit the changes made on setup to a sandboxed
DemoStorage that uses the previous ZODB storage as a base storgae.  On
tear down, the layer will restore the base storage.  This allows the
layer to use and commit changes to a fully functional ZODB while
isolating the effects of the layer from any parent or sibling layers.

As one would expect, layers that use the sandboxed layer as a base
layer will see the ZODB according the base layer.  Additionally,
sandboxed layers can use other sandboxed layers as base layers, thus
allowing for nested but isolated ZODB sandboxes.

Create a sandboxed layer.  Layers that subclass Sandboxed should
implement an afterSetUp method to do any changes for the layer.
Additionally, such layers may also provide a beforeTearDown method to
tear down any changes made by the layer that won't be cleaned up by
restoring the ZODB.

    >>> from collective.testcaselayer import ztc
    >>> class FooLayer(ztc.BaseZTCLayer):
    ...     def afterSetUp(self):
    ...         self.app.foo = 'foo'
    >>> foo_layer = FooLayer()

Before the layer is set up, the ZODB doesn't reflect the layer's
changes.

    >>> from Testing import ZopeTestCase
    >>> app = ZopeTestCase.app()
    >>> getattr(app, 'foo', None)
    >>> ZopeTestCase.close(app)

After the layer is set up, the changes have been committed to the
ZODB.

    >>> foo_layer.setUp()

    >>> app = ZopeTestCase.app()
    >>> getattr(app, 'foo', None)
    'foo'
    >>> ZopeTestCase.close(app)

Create a sandboxed layer that uses the first layer as a base layer.

    >>> class BarLayer(ztc.BaseZTCLayer):
    ...     def afterSetUp(self):
    ...         self.app.bar = 'bar'
    >>> bar_layer = BarLayer([foo_layer])

Before the sub-layer is set up, the ZODB still reflects the base
layer's changes but not the sub-layer's changes.

    >>> app = ZopeTestCase.app()
    >>> getattr(app, 'foo', None)
    'foo'
    >>> getattr(app, 'bar', None)
    >>> ZopeTestCase.close(app)

After the sub-layer is set up, the ZODB reflects the changes from both
layers.

    >>> bar_layer.setUp()

    >>> app = ZopeTestCase.app()
    >>> getattr(app, 'foo', None)
    'foo'
    >>> getattr(app, 'bar', None)
    'bar'
    >>> ZopeTestCase.close(app)

Any test case using Testing.ZopeTestCase.sandbox.Sandboxed, such as
zope.testbrowser tests run against Zope2, calls the ZopeLite.sandbox()
function without any arguments.  In such cases, the resulting per-test
sandboxed ZODB will still be based on the layer sandboxed ZODB.

    >>> app = ZopeTestCase.Zope2.app(
    ...     ZopeTestCase.Zope2.sandbox().open())
    >>> getattr(app, 'foo', None)
    'foo'
    >>> getattr(app, 'bar', None)
    'bar'
    >>> app._p_jar.close()

After the sub-layer is torn down, the ZODB reflects only the changes
from the base layer.

    >>> bar_layer.tearDown()

    >>> app = ZopeTestCase.app()
    >>> getattr(app, 'foo', None)
    'foo'
    >>> getattr(app, 'bar', None)
    >>> ZopeTestCase.close(app)

After the base layer is torn down, the ZODB doesn't reflect the changes
from either layer.

    >>> foo_layer.tearDown()

    >>> app = ZopeTestCase.app()
    >>> getattr(app, 'foo', None)
    >>> getattr(app, 'bar', None)
    >>> ZopeTestCase.close(app)
