from Products.CMFTestCase import ctc

from collective.testcaselayer import ztc


class CTCLayer(ztc.TestCaseLayer, ctc.CMFTestCase):
    """CMFTestCase as a sandboxed layer."""
    pass

ctc_layer = CTCLayer([ctc.CMFTestCase.layer])


class BaseCTCLayer(ztc.BasePTCLayerMixin, CTCLayer):
    """Sandboxed layer base class with CMFTestCase facilities."""
    pass
