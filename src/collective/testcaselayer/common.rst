.. -*-doctest-*-

Common Layer
============

If a testing layer uses the
collective.testcaselayer.common.common_layer as a base layer then a
few commonly useful things will be set up.

Before setting up the layer, the default exceptions are ignored in the
error_log and the resource registries are not in debug mode.

    >>> portal.error_log.getProperties()['ignored_exceptions']
    ('Unauthorized', 'NotFound', 'Redirect')

    >>> portal.portal_css.getDebugMode()
    False
    >>> portal.portal_javascripts.getDebugMode()
    False
    >>> portal.portal_kss.getDebugMode()
    False

Set up the common_layer.

    >>> from zope.testing.testrunner import runner
    >>> from collective.testcaselayer import common

    >>> def getSetUpLayers(layer):
    ...     for base in layer.__bases__:
    ...         if base is not object:
    ...             for recurs in getSetUpLayers(base):
    ...                 yield recurs
    ...             yield base
    >>> setup_layers = dict((layer, 1) for layer in
    ...                     getSetUpLayers(common.common_layer))

    >>> options = runner.get_options([], [])
    >>> runner.setup_layer(options, common.common_layer, setup_layers)
    Set up collective.testcaselayer.common.CommonPTCLayer in ... seconds.

Now only 'Redirect' is ignored in error_log, and the resources
registries are in debug mode.

    >>> from Testing import ZopeTestCase
    >>> from Products.PloneTestCase import ptc as plone_ptc
    >>> app = ZopeTestCase.app()
    >>> portal = getattr(app, plone_ptc.portal_name)

    >>> portal.error_log.getProperties()['ignored_exceptions']
    ('Redirect',)

    >>> portal.portal_css.getDebugMode()
    True
    >>> portal.portal_javascripts.getDebugMode()
    True
    >>> portal.portal_kss.getDebugMode()
    True
