from Testing import ZopeTestCase

from collective.testcaselayer import testcase, sandbox

class TestCaseLayer(testcase.TestCaseLayer):

    def _setup(self):
        super(TestCaseLayer, self)._setup()
        self.logout()

    def _close(self):
        super(TestCaseLayer, self)._close()
        del self.app

class ZTCLayer(TestCaseLayer, ZopeTestCase.ZopeTestCase):
    """ZopeTestCase as a layer."""
    pass

ztc_layer = ZTCLayer()

class ZTCSandboxedLayer(sandbox.Sandboxed, ZTCLayer):
    """ZopeTestCase as a sandboxed layer."""
    pass

ztc_sandboxed_layer = ZTCSandboxedLayer()

class PTCLayer(TestCaseLayer, ZopeTestCase.PortalTestCase):
    """PortalTestCase as a layer."""
    pass

ptc_layer = PTCLayer()

class PTCSandboxedLayer(sandbox.Sandboxed, PTCLayer):
    """PortalTestCase as a sandboxed layer."""
    pass

ptc_sandboxed_layer = PTCSandboxedLayer()

class BaseZTCLayerMixin(object):
    """ZTC layer mixin without setting up the test fixture."""
    
    _setup_fixture = False

    @property
    def folder(self):
        return getattr(self.app, ZopeTestCase.folder_name)
    
class BasePTCLayerMixin(object):
    """PTC layer mixin without configuring the portal."""

    _configure_portal = False

class BaseZTCLayer(BaseZTCLayerMixin, ZTCLayer):
    """Layer base class with ZopeTestCase facilities."""
    pass

class BaseZTCSandboxedLayer(BaseZTCLayerMixin, ZTCSandboxedLayer):
    """Sandboxed layer base class with ZopeTestCase facilities."""
    pass

class BasePTCLayer(BasePTCLayerMixin, PTCLayer):
    """Layer base class with PortalTestCase facilities."""
    pass

class BasePTCSandboxedLayer(BasePTCLayerMixin, PTCSandboxedLayer):
    """Sandboxed layer base class with PortalTestCase facilities."""
    pass
