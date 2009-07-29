from Products.PloneTestCase import ptc

from collective.testcaselayer import ztc

ptc.setupPloneSite()

class PTCLayer(ztc.TestCaseLayer, ptc.PloneTestCase):
    """PloneTestCase as a sandboxed layer."""
    pass

ptc_layer = PTCLayer([ptc.PloneTestCase.layer])

class BasePTCLayer(ztc.BasePTCLayerMixin, PTCLayer):
    """Sandboxed layer base class with PloneTestCase facilities."""
    pass
