import os
import sys

from Testing import ZopeTestCase
USE_ZOPELITE = True
try:
    from Testing.ZopeTestCase import layer
except ImportError:
    USE_ZOPELITE = False  # BBB Zope <2.12

import Products

from collective.testcaselayer import ztc
from collective.testcaselayer.testing import CollectiveTestCaseLayerTesting

path = os.path.dirname(os.path.dirname(
    CollectiveTestCaseLayerTesting.__file__))


class ProductLayer(ztc.BaseZTCLayer):

    def setUp(self):
        Products.__path__.append(path)
        ZopeTestCase.installProduct('CollectiveTestCaseLayerTesting')
        if USE_ZOPELITE:  # BBB Zope <2.12
            layer.ZopeLite.setUp()
        super(ProductLayer, self).setUp()

    def tearDown(self):
        super(ProductLayer, self).tearDown()
        for module in sys.modules.keys():
            if module.startswith(
                'Products.CollectiveTestCaseLayerTesting'):
                del sys.modules[module]
        Products.__path__.remove(path)

product_layer = ProductLayer()
