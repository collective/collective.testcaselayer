from zope.interface import interfaces
from zope import interface

from ZPublisher.Iterators import IStreamIterator


class StreamIterator(list):
    if interfaces.IInterface.providedBy(IStreamIterator):
        interface.implements(IStreamIterator)
    else:
        __implements__ = (IStreamIterator, )  # BBB Plone 3
