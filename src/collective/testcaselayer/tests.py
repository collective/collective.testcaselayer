import unittest
import doctest
from Testing.ZopeTestCase.zopedoctest import functional

from Products.PloneTestCase import ptc

import sys
from collective import testcaselayer
from collective.testcaselayer import mail

# stub out a collective.foo modulte
sys.modules['collective.foo'] = testcaselayer

optionflags = (doctest.NORMALIZE_WHITESPACE |
               doctest.ELLIPSIS |
               doctest.REPORT_NDIFF)


def test_suite():
    doc_suite = doctest.DocFileSuite(
        'README.rst',
        'layer.rst',
        'sandbox.rst',
        'ztc.rst',
        'ctc.rst',
        'ptc.rst',
        optionflags=optionflags)
    func_suite = functional.FunctionalDocFileSuite(
        'functional.rst',
        optionflags=optionflags)
    mail_suite = functional.FunctionalDocFileSuite(
        'mail.rst',
        'common.rst',
        optionflags=optionflags,
        test_class=ptc.FunctionalTestCase)
    mail_suite.layer = mail.mockmailhost_layer
    return unittest.TestSuite((doc_suite, func_suite, mail_suite))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
