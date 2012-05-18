.. -*-doctest-*-

collective.testcaselayer.ctc
============================

The collective.testcaselayer.ctc module extends the layers and layer
base classes from collective.testcaselayer.ztc to CMFTestCase.  See
ztc.txt for an introduction to using the layers and layer base
classes.  Here we will only demonstrate that the facilities specific
to CMFTestCase not inherited from ZopeTestCase.

Layers
------

The CMFTestCase test fixture can be set up and torn down as a layer.

    >>> from collective.testcaselayer import ctc
    >>> ctc.ctc_layer
    <collective.testcaselayer.ctc.CTCLayer testMethod=layerOnly>

To test the effects of just this layer, set up the base layer
separately.  Because of the way CMFTestCase uses layers, we must first
call the setupCMFSite() function.

    >>> from zope.testing.testrunner import runner
    >>> from Products.CMFTestCase import ctc as cmf_ctc
    >>> cmf_ctc.setupCMFSite()
    >>> cmfsite_layer, = ctc.ctc_layer.__bases__
    >>> options = runner.get_options([], [])
    >>> setup_layers = {}
    >>> runner.setup_layer(options, cmfsite_layer, setup_layers)
    Set up...Products.CMFTestCase.layer.ZCML in ... seconds.
    Set up Products.CMFTestCase.layer.CMFSite in ... seconds.

The CMFTestCase test fixture has not been set up.

    >>> from Testing import ZopeTestCase
    >>> app = ZopeTestCase.app()
    >>> portal = getattr(app, cmf_ctc.portal_name)
    >>> portal.acl_users.getUserById(cmf_ctc.default_user)
    >>> hasattr(portal.Members, cmf_ctc.default_user)
    False
    >>> ZopeTestCase.close(app)

Set up the CMFTestCase layer.

    >>> runner.setup_layer(options, ctc.ctc_layer, setup_layers)
    Set up collective.testcaselayer.ctc.CTCLayer in ... seconds.

The CMFTestCase test fixture has been set up.

    >>> app = ZopeTestCase.app()
    >>> portal = getattr(app, cmf_ctc.portal_name)
    >>> portal.acl_users.getUserById(cmf_ctc.default_user)
    <User 'test_user_1_'>
    >>> getattr(portal.Members, cmf_ctc.default_user)
    <PortalFolder at /cmf/Members/test_user_1_>
    >>> ZopeTestCase.close(app)

Tear down the CMFTestCase layer.

    >>> runner.tear_down_unneeded(
    ...     options,
    ...     [layer for layer in setup_layers
    ...      if layer is not ctc.ctc_layer],
    ...     setup_layers)
    Tear down collective.testcaselayer.ctc.CTCLayer in ... seconds.

The CMFTestCase test fixture is no longer set up.

    >>> app = ZopeTestCase.app()
    >>> portal = getattr(app, cmf_ctc.portal_name)
    >>> portal.acl_users.getUserById(cmf_ctc.default_user)
    >>> hasattr(portal.Members, cmf_ctc.default_user)
    False
    >>> ZopeTestCase.close(app)

Layer Base Classes
------------------

The CMFTestCase class facilities can also be used in layers that use
the CMFTestCase layer base class.

    >>> class FooLayer(ctc.BaseCTCLayer):
    ...     def afterSetUp(self):
    ...         self.addProfile(
    ...             'Products.CMFDefault:sample_content')
    ...         self.addProduct('CollectiveTestCaseLayerTesting')
    ...         self.loginAsPortalOwner()

This layer depends on the profile and product added which are set up
in a testing only layer.

    >>> from collective.testcaselayer.testing import layer
    >>> foo_layer = FooLayer([layer.product_layer, ctc.ctc_layer])

The FooLayer test fixture has not been set up.

    >>> app = ZopeTestCase.app()
    >>> portal = getattr(app, cmf_ctc.portal_name)

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
    >>> portal = getattr(app, cmf_ctc.portal_name)

    >>> portal.subfolder
    <PortalFolder at /cmf/subfolder>
    >>> portal.foo
    'foo'

    >>> from AccessControl import SecurityManagement
    >>> SecurityManagement.getSecurityManager().getUser().getId()
    'portal_owner'

    >>> ZopeTestCase.close(app)

The convenience attributes of the PortalTestCase are available.

    >>> foo_layer.folder
    <PortalFolder at /cmf/Members/test_user_1_>

Tear down the FooLayer.

    >>> runner.tear_down_unneeded(
    ...     options,
    ...     [layer for layer in setup_layers
    ...      if layer is not foo_layer],
    ...     setup_layers)
    Tear down FooLayer in ... seconds.

The FooLayer test fixture is no longer set up.

    >>> app = ZopeTestCase.app()
    >>> portal = getattr(app, cmf_ctc.portal_name)

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
    Tear down Products.CMFTestCase.layer.CMFSite in ... seconds.
    Tear down Products.CMFTestCase.layer.ZCML in ... seconds.
