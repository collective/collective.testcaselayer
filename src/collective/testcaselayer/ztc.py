from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from collective.testcaselayer import testcase, sandbox

# The base class does cleanup on setUp failure since test case
# tearDown doesn't get run if setUp failures.  But under
# zope.testing.testrunner, layer tearDown does get run even if layer
# setUp fails.

class TestCaseLayer(sandbox.Sandboxed, testcase.TestCaseLayer):

    def _close(self):
        super(TestCaseLayer, self)._close()
        del self.app

    def loadZCML(self, file_, **kw):
        fiveconfigure.debug_mode = True
        try:
            zcml.load_config(file_, **kw)
        finally:
            fiveconfigure.debug_mode = False


class ZopeTestCase(ztc.ZopeTestCase):

    def setUp(self):
        """Let layer tear down do cleanup and logout after setup."""
        self.beforeSetUp()
        self.app = self._app()
        self._setup()
        self.logout()
        self.afterSetUp()
    

class ZTCLayer(TestCaseLayer, ZopeTestCase):
    """ZopeTestCase as a sandboxed layer."""
    pass

ztc_layer = ZTCLayer()


class PortalTestCase(ztc.PortalTestCase):

    def setUp(self):
        """Let layer tear down do cleanup and logout after setup."""
        self.beforeSetUp()
        self.app = self._app()
        self.portal = self._portal()
        self._setup()
        self.logout()
        self.afterSetUp()


class PTCLayer(TestCaseLayer, PortalTestCase):
    """PortalTestCase as a sandboxed layer."""
    pass

ptc_layer = PTCLayer()


class BaseZTCLayerMixin(object):
    """ZTC layer mixin without setting up the test fixture."""

    _setup_fixture = False

    @property
    def folder(self):
        return getattr(self.app, ztc.folder_name)


class BasePTCLayerMixin(object):
    """PTC layer mixin without configuring the portal."""

    _configure_portal = False

    @property
    def folder(self):
        return self.portal.portal_membership.getHomeFolder(ztc.user_name)


class BaseZTCLayer(BaseZTCLayerMixin, ZTCLayer):
    """Sandboxed layer base class with ZopeTestCase facilities."""
    pass


class BasePTCLayer(BasePTCLayerMixin, PTCLayer):
    """Sandboxed layer base class with PortalTestCase facilities."""
    pass
