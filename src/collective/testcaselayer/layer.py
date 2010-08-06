import sys


class Layer(object):
    """A layer instantiated with base layers."""

    def __init__(self, bases=(), module=None, name=None):
        if self.__class__ is Layer:
            if module is None:
                caller_globals = sys._getframe(1).f_globals
                module = caller_globals['__name__']
            if name is None:
                raise ValueError(
                    'The "name" argument is requied when '
                    'instantiating "Layer" directly')

        if module is not None:
            self.__module__ = module
        else:
            self.__module__ = self.__class__.__module__

        if name is not None:
            self.__name__ = name
        else:
            self.__name__ = self.__class__.__name__

        self.__bases__ = tuple(bases)
