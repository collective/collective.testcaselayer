from Products.PloneTestCase import ptc
from Products.PloneTestCase import layer

from collective.testcaselayer import ztc

ptc.setupPloneSite()


class PTCLayer(ztc.TestCaseLayer, ptc.PloneTestCase):
    """PloneTestCase as a sandboxed layer."""
    pass

ptc_layer = PTCLayer([layer.PloneSite])


class BasePTCLayer(ztc.BasePTCLayerMixin, PTCLayer):
    """Sandboxed layer base class with PloneTestCase facilities."""
    pass
