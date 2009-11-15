from ZPublisher.Iterators import IStreamIterator

class StreamIterator(list):
    __implements__ = (IStreamIterator,)
