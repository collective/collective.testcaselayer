"""zope.testing layers with Zope 2 ZODB sandboxes"""

import transaction

import Zope2
from App import ZApplication

from Testing import ZopeTestCase

orig_app = ZopeTestCase.Zope2.app

class Sandboxed(object):

    def _app(self):
        self.orig_bobo_application = Zope2.bobo_application
        db, name, version_cookie_name = (
            self.orig_bobo_application._stuff)
        sandboxed_db = ZopeTestCase.Zope2.sandbox(db)
        Zope2.bobo_application = ZApplication.ZApplicationWrapper(
            sandboxed_db, name,
            klass=self.orig_bobo_application._klass,
            version_cookie_name=version_cookie_name)
        return super(Sandboxed, self)._app()

    def _close(self):
        Zope2.bobo_application = self.orig_bobo_application
        return super(Sandboxed, self)._close()
    
    def setUp(self):
        """Commit results after setup."""
        result = super(Sandboxed, self).setUp()
        transaction.commit()
        return result
