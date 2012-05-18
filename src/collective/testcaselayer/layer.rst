.. -*-doctest-*-

collective.testcaselayer.layer
==============================

In many cases, classes can be used as layers themselves where the base
classes are used as the base layers.  This means that the layer
inheritance herirarchy, used for code factoring and re-use, becomes
bound to the layer set up heirachy, used to determine which layers are
set up when and for which tests.  IOW, it is not possible for a layer
to subclass another layer *just* to re-use functionality without also
depending on that layer being set up as well.  Additionally, when
using classes as layers, all layer methods (setUp, tearDown,
testSetUp, and testTearDown) must be defined on class layers with base
classes to avoid accidentally running the method of a base class/layer
at the wrong time.

The collective.testcaselayer.layer module provides a Layer class
intended to be used as a base class for classes whoss instances will
be layers.  Instances of this class can also be used directly solely
to group layers together into one layer.

    >>> from collective.testcaselayer import layer

Layer Classes
-------------

Use the collective.testcaselayer.layer.Layer class to create your own
layer classes.

    >>> class FooLayer(layer.Layer):
    ...     def setUp(self): print 'running FooLayer.setUp'

The instances of the class will be your actual zope.testing layer.

    >>> foo_layer = FooLayer()

    >>> from zope.testing.testrunner import runner
    >>> options = runner.get_options([], [])
    >>> runner.setup_layer(options, foo_layer, {})
    Set up FooLayer running FooLayer.setUp
    in ... seconds.

Beware that the Layer class itself or subclasses can be used
themselves as layers without error but that is not how they're
intended to be used.  For example, using the FooLayer class as a layer
will treat the Layer base class as a layer itself and will set it up
which is meaningless.  Further, it will try to call the setUp method
as a class method which will raise an error.

    >>> runner.setup_layer(options, FooLayer, {})
    Traceback (most recent call last):
    TypeError: unbound method setUp() must be called with FooLayer instance as first argument (got nothing instead)

Base Layers
-----------

Base layers are designated by passing them into the layer class on
instantiation.

Create another layer class.

    >>> class BarLayer(layer.Layer):
    ...     def setUp(self): print 'running BarLayer.setUp'

Create the new layer that uses foo_layer as a base layer.

    >>> bar_layer = BarLayer([foo_layer])

Set up the layers.

    >>> runner.setup_layer(options, bar_layer, {})
    Set up FooLayer running FooLayer.setUp
    in ... seconds.
    Set up BarLayer running BarLayer.setUp
    in ... seconds.

Grouping Layers
---------------

If all that's required from a layer is that it groups other layers as
base layers, then the collective.testcaselayer.layer.Layer class can
be used directly.

Create another layer.

    >>> class BazLayer(layer.Layer):
    ...     def setUp(self): print 'running BazLayer.setUp'
    >>> baz_layer = BazLayer()

Instantiate the Layer class with the base layers, a module, and a name.

    >>> qux_layer = layer.Layer(
    ...     [bar_layer, baz_layer],
    ...     module='QuxModule', name='QuxLayer')

Set up the layers.

    >>> runner.setup_layer(options, qux_layer, {})
    Set up FooLayer running FooLayer.setUp
    in ... seconds.
    Set up BarLayer running BarLayer.setUp
    in ... seconds.
    Set up BazLayer running BazLayer.setUp
    in ... seconds.
    Set up QuxModule.QuxLayer in ... seconds.

By default, layers have the same module and name as their class.  If
you want the layer to have a different module or name than the class,
then the both can be passed in as arguments.  This is useful in this
case and any time multiple instances of the same layer class will be
used as layers.

Instantiating the Layer class directly without passing a name raises
an error.

    >>> layer.Layer([], module='QuxModule')
    Traceback (most recent call last):
    ValueError: The "name" argument is requied when instantiating
    "Layer" directly

If the Layer class is instantiated directly without passing a module,
the module name from the calling frame is used.

    >>> __name__ = 'BahModule'
    >>> quux_layer = layer.Layer([], name='QuuxLayer')
    >>> runner.setup_layer(options, quux_layer, {})
    Set up BahModule.QuuxLayer in ... seconds.
