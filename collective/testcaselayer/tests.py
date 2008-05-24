import unittest
from zope.testing import doctest

optionflags = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF)

def test_suite():
    return doctest.DocFileSuite(
        'layer.txt',
        'sandbox.txt',
        'ztc.txt',
        'ctc.txt',
        'ptc.txt',
        optionflags=optionflags)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
