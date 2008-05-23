import os

import Products
from Products.CMFTestCase import layer

from collective.testcaselayer import ctc
from collective.testcaselayer.testing import CollectiveTestCaseLayerTesting

path = os.path.dirname(os.path.dirname(
    CollectiveTestCaseLayerTesting.__file__))

class CMFLayer(ctc.BaseCTCLayer):

    def afterSetUp(self):
        Products.__path__.append(path)

    def beforeTearDown(self):
        Products.__path__.remove(path)

cmf_layer = CMFLayer([layer.ZCML])
