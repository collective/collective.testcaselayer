import unittest

from collective.testcaselayer import layer


class TestCaseLayer(layer.Layer):
    """Mixin class for turning unittest TestCase classes into layer
    classes."""

    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, methodName='layerOnly')
        super(TestCaseLayer, self).__init__(*args, **kw)

    def layerOnly(self):
        """Used only as a zope.testing layer, not a test."""
        pass
