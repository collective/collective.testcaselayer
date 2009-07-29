import unittest
from zope.testing import doctest

import sys
from collective import testcaselayer

# stub out a collective.foo modulte
sys.modules['collective.foo'] = testcaselayer

optionflags = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF)

def test_suite():
    return doctest.DocFileSuite(
        'README.txt',
        'layer.txt',
        'sandbox.txt',
        'ztc.txt',
        'ctc.txt',
        'ptc.txt',
        optionflags=optionflags)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
