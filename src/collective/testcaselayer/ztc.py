from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase

from collective.testcaselayer import testcase, sandbox

class TestCaseLayer(sandbox.Sandboxed, testcase.TestCaseLayer):

    def _setup(self):
        super(TestCaseLayer, self)._setup()
        self.logout()

    def _close(self):
        super(TestCaseLayer, self)._close()
        del self.app

    def loadZCML(self, file_, **kw):
        fiveconfigure.debug_mode = True
        zcml.load_config(file_, **kw)
        fiveconfigure.debug_mode = False

class ZTCLayer(TestCaseLayer, ZopeTestCase.ZopeTestCase):
    """ZopeTestCase as a sandboxed layer."""
    pass

ztc_layer = ZTCLayer()

class PTCLayer(TestCaseLayer, ZopeTestCase.PortalTestCase):
    """PortalTestCase as a sandboxed layer."""
    pass

ptc_layer = PTCLayer()

class BaseZTCLayerMixin(object):
    """ZTC layer mixin without setting up the test fixture."""
    
    _setup_fixture = False

    @property
    def folder(self):
        return getattr(self.app, ZopeTestCase.folder_name)
    
class BasePTCLayerMixin(object):
    """PTC layer mixin without configuring the portal."""

    _configure_portal = False

    @property
    def folder(self):
        return self.portal.portal_membership.getHomeFolder(
            ZopeTestCase.user_name)

class BaseZTCLayer(BaseZTCLayerMixin, ZTCLayer):
    """Sandboxed layer base class with ZopeTestCase facilities."""
    pass

class BasePTCLayer(BasePTCLayerMixin, PTCLayer):
    """Sandboxed layer base class with PortalTestCase facilities."""
    pass
