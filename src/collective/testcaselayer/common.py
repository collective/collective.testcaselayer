from collective.testcaselayer import ptc
from collective.testcaselayer import mail


class CommonPTCLayer(ptc.BasePTCLayer):
    """A layer with some common useful testing and debugging setup."""

    def afterSetUp(self):
        """Apply some useful testing and debugging changes"""

        # Don't ignore exceptions so that problems don't hide behind
        # Unauthorized or NotFound exceptions when doing functional
        # testing.
        error_props = self.portal.error_log.getProperties()
        error_props['ignored_exceptions'] = ('Redirect',)
        error_props = self.portal.error_log.setProperties(
            **error_props)

        # Put resource registries in debug mode to make it easier to
        # inspect CSS, JavaScript, and KSS
        self.portal.portal_css.setDebugMode(True)
        self.portal.portal_javascripts.setDebugMode(True)
        portal_kss = self.portal.get('portal_kss')
        if portal_kss is not None:
            portal_kss.setDebugMode(True)

common_layer = CommonPTCLayer([mail.mockmailhost_layer])
