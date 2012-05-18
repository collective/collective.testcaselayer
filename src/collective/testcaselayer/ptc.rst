.. -*-doctest-*-

collective.testcaselayer.ptc
============================

The collective.testcaselayer.ptc module extends the layers and layer
base classes from collective.testcaselayer.ztc to PloneTestCase.  See
ztc.txt for an introduction to using the layers and layer base
classes.  Here we will only demonstrate that the facilities specific
to PloneTestCase not inherited from ZopeTestCase.

Layers
------

The PloneTestCase test fixture can be set up and torn down as a layer.

    >>> from collective.testcaselayer import ptc
    >>> ptc.ptc_layer
    <collective.testcaselayer.ptc.PTCLayer testMethod=layerOnly>

To test the effects of just this layer, set up the base layer
separately.  Because of the way PloneTestCase uses layers, we must first
call the setupPloneSite() function.

    >>> from zope.testing.testrunner import runner
    >>> from Products.PloneTestCase import ptc as plone_ptc
    >>> plonesite_layer, = ptc.ptc_layer.__bases__
    >>> options = runner.get_options([], [])
    >>> setup_layers = {}
    >>> runner.setup_layer(options, plonesite_layer, setup_layers)
    Set up...Products.PloneTestCase.layer.ZCML in ... seconds.
    Set up Products.PloneTestCase.layer.PloneSite in ... seconds.

The PloneTestCase test fixture has not been set up.

    >>> from Testing import ZopeTestCase
    >>> app = ZopeTestCase.app()
    >>> portal = getattr(app, plone_ptc.portal_name)
    >>> portal.acl_users.getUserById(plone_ptc.default_user)
    >>> ZopeTestCase.close(app)

Set up the PloneTestCase layer.

    >>> runner.setup_layer(options, ptc.ptc_layer, setup_layers)
    Set up collective.testcaselayer.ptc.PTCLayer in ... seconds.

The PloneTestCase test fixture has been set up.

    >>> app = ZopeTestCase.app()
    >>> portal = getattr(app, plone_ptc.portal_name)
    >>> portal.acl_users.getUserById(plone_ptc.default_user)
    <PloneUser 'test_user_1_'>
    >>> ZopeTestCase.close(app)

Tear down the PloneTestCase layer.

    >>> runner.tear_down_unneeded(
    ...     options,
    ...     [layer for layer in setup_layers
    ...      if layer is not ptc.ptc_layer],
    ...     setup_layers)
    Tear down collective.testcaselayer.ptc.PTCLayer in ... seconds.

The PloneTestCase test fixture is no longer set up.

    >>> app = ZopeTestCase.app()
    >>> portal = getattr(app, plone_ptc.portal_name)
    >>> portal.acl_users.getUserById(plone_ptc.default_user)
    >>> ZopeTestCase.close(app)

Layer Base Classes
------------------

The PloneTestCase class facilities can also be used in layers that use
the PloneTestCase layer base class.

    >>> class FooLayer(ptc.BasePTCLayer):
    ...     def afterSetUp(self):
    ...         self.addProfile(
    ...             'Products.CMFDefault:sample_content')
    ...         self.addProduct('CollectiveTestCaseLayerTesting')
    ...         self.loginAsPortalOwner()

This layer depends on the profile and product added which are set up
in a testing only layer.

    >>> from collective.testcaselayer.testing import layer
    >>> foo_layer = FooLayer([layer.product_layer, ptc.ptc_layer])

The FooLayer test fixture has not been set up.

    >>> app = ZopeTestCase.app()
    >>> portal = getattr(app, plone_ptc.portal_name)

    >>> hasattr(portal, 'subfolder')
    False
    >>> hasattr(portal, 'foo')
    False

    >>> from AccessControl import SecurityManagement
    >>> SecurityManagement.getSecurityManager().getUser()
    <SpecialUser 'Anonymous User'>

    >>> ZopeTestCase.close(app)

Set up the FooLayer.

    >>> runner.setup_layer(options, foo_layer, setup_layers)
    Set up collective.testcaselayer.testing.layer.ProductLayer
    in ... seconds.
    Set up FooLayer in ... seconds.

The FooLayer test fixture has been set up.

    >>> app = ZopeTestCase.app()
    >>> portal = getattr(app, plone_ptc.portal_name)

    >>> portal.subfolder
    <ATFolder at /plone/subfolder>
    >>> portal.foo
    'foo'

    >>> from AccessControl import SecurityManagement
    >>> SecurityManagement.getSecurityManager().getUser()
    <PropertiedUser 'portal_owner'>

    >>> ZopeTestCase.close(app)

Tear down the FooLayer.

    >>> runner.tear_down_unneeded(
    ...     options,
    ...     [layer for layer in setup_layers
    ...      if layer is not foo_layer],
    ...     setup_layers)
    Tear down FooLayer in ... seconds.

The FooLayer test fixture is no longer set up.

    >>> app = ZopeTestCase.app()
    >>> portal = getattr(app, plone_ptc.portal_name)

    >>> hasattr(portal, 'subfolder')
    False
    >>> hasattr(portal, 'foo')
    False

    >>> from AccessControl import SecurityManagement
    >>> SecurityManagement.getSecurityManager().getUser()
    <SpecialUser 'Anonymous User'>

    >>> ZopeTestCase.close(app)

Finish tearing down the rest of the layers.

    >>> runner.tear_down_unneeded(options, [], setup_layers)
    Tear down collective.testcaselayer.testing.layer.ProductLayer
    in ... seconds.
    Tear down Products.PloneTestCase.layer.PloneSite in ... seconds.
    Tear down Products.PloneTestCase.layer.ZCML in ... seconds.
