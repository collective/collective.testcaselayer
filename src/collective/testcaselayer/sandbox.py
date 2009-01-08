"""zope.testing layers with Zope 2 ZODB sandboxes"""

import transaction

import Zope2
from App import ZApplication

from Testing import ZopeTestCase

orig_app = ZopeTestCase.Zope2.app

class Sandboxed(object):

    def _app(self):
        self.orig_bobo_application = Zope2.bobo_application
        self.orig_db = Zope2.DB
        db, name, version_cookie_name = (
            self.orig_bobo_application._stuff)
        new_db = self._getNewDB(db)
        Zope2.DB = new_db
        Zope2.bobo_application = ZApplication.ZApplicationWrapper(
            new_db, name,
            klass=self.orig_bobo_application._klass,
            version_cookie_name=version_cookie_name)
        return super(Sandboxed, self)._app()

    def _getNewDB(self, db):
        return ZopeTestCase.Zope2.sandbox(db)

    def _close(self):
        Zope2.DB = self.orig_db
        Zope2.bobo_application = self.orig_bobo_application
        return super(Sandboxed, self)._close()
    
    def setUp(self):
        """Commit results after setup."""
        result = super(Sandboxed, self).setUp()
        transaction.commit()
        return result

# XXX Untested
def committer(method):
    """A decorator for methods that commit changes to the app."""

    def __call__(self, *args, **kw):
        self.app = ZopeTestCase.app()
        try:
            transaction.begin()
            try:
                result = method(*args, **kw)
            except:
                transaction.abort()
                raise
            else:
                transaction.commit()
            return result
        finally:
            ZopeTestCase.close(self.app)
            del self.app

    return __call__
