.. -*-doctest-*-

collective.testcaselayer.ztc
============================

The BaseZTCLayer and cousins are intended to be used as base classes
for layers to allow them to use the facilities of ZopeTestCase,
PortalTestCase, and their subclasses.  Thus, the layer setUp and
tearDown methods can use the test case methods and other support such
as: self.login(), self.logout(), self.loginAsPortalOwner(),
self.setRoles(), self.setPermissions(), etc..

The ZTCLayer and cousins allow using the test fixture setup by any of
the test cases as a layer itself.

The collective.testcaselayer.ctc and collective.testcaselayer.ptc
modules extend this support to CMFTestCase and PloneTestCase, though
collective.testcaselayer does not depend on them itself.  These layer
base classes allow for use of those test cases' methods such as
addProfile() and addProduct() see ctc.txt and ptc.txt for more
details.

Layers
------

The collective.testcaselayer.ztc module provides sandboxed layers that
set up the test fixtures for ZopeTestCase.  Note that test case based
layers still act like test cases with a special no-op layerOnly() test
method to that they have functional str() and repr() values.

    >>> from collective.testcaselayer import ztc
    >>> ztc.ztc_layer
    <collective.testcaselayer.ztc.ZTCLayer testMethod=layerOnly>

Before we set up ZopeTestCase as a layer, nothing has been set up.

    >>> from AccessControl import SecurityManagement
    >>> SecurityManagement.getSecurityManager().getUser()
    <SpecialUser 'Anonymous User'>

    >>> hasattr(ztc.ztc_layer, 'app')
    False

    >>> from Testing import ZopeTestCase
    >>> app = ZopeTestCase.app()
    >>> 'test_folder_1_' in app.objectIds()
    False
    >>> ZopeTestCase.close(app)

    >>> from Testing.ZopeTestCase import connections
    >>> connections.count()
    0

Set up ZopeTestCase as a layer.

    >>> from zope.testing.testrunner import runner
    >>> options = runner.get_options([], [])
    >>> setup_layers = {}
    >>> runner.setup_layer(options, ztc.ztc_layer, setup_layers)
    Set up collective.testcaselayer.ztc.ZTCLayer in ... seconds.

The ZopeTestCase test fixture has been set up, but there is no logged
in user.

    >>> SecurityManagement.getSecurityManager().getUser()
    <SpecialUser 'Anonymous User'>

    >>> 'test_folder_1_' in  ztc.ztc_layer.app.objectIds()
    True

Also note that the app attribute of the layer represents an open
connection to the ZODB.

    >>> connections.count()
    1

Tear down the ZopeTestCase layer.

    >>> runner.tear_down_unneeded(options, [], setup_layers)
    Tear down collective.testcaselayer.ztc.ZTCLayer in ... seconds.

Now everything is back to its previous state.

    >>> SecurityManagement.getSecurityManager().getUser()
    <SpecialUser 'Anonymous User'>

    >>> hasattr(ztc.ztc_layer, 'app')
    False

    >>> from Testing import ZopeTestCase
    >>> app = ZopeTestCase.app()
    >>> 'test_folder_1_' in app.objectIds()
    False
    >>> ZopeTestCase.close(app)

    >>> connections.count()
    0

Layer Base Classes
------------------

The collective.testcaselayer.ztc module also provides base classes for
sandboxed layers that don't actually set up the test case fixtures but
allow using the facilities provided by the test cases in the layer set
up and tear down code.

Since layers can be nested, these layer base classes don't do the
actual ZopeTestCase test fixture set up unless a subclass explicitly
sets _setup_fixture (or _configure_portal for PortalTestCase) to True.
Best practice should be to instantiate any layers depending on the ZTC
test fixture with the ZTCLayer as a base layer as above.

Create a layer class that subclasses the appropriate base layer class.
This layer class overrides the afterSetUp() method just as with
ZopeTestCase based test cases.  The afterSetUp method here excercises
the factilities provided by ZopeTestCase and an additional loadZCML()
method for loading ZCML files with ZCML debug mode enabled.

    >>> from collective.testcaselayer import testing
    >>> class FooLayer(ztc.BaseZTCLayer):
    ...     def afterSetUp(self):
    ...         self.login()
    ...         self.setRoles(['Manager'])
    ...         self.loadZCML('loadzcml.zcml', package=testing)
    >>> foo_layer = FooLayer([ztc.ztc_layer])

To test the effects of just this layer, set up the base layer
separately.

    >>> runner.setup_layer(options, ztc.ztc_layer, setup_layers)
    Set up collective.testcaselayer.ztc.ZTCLayer in ... seconds.

Before setting up the new layer, only the ZopeTestCase fixture is set
up.

    >>> SecurityManagement.getSecurityManager().getUser()
    <SpecialUser 'Anonymous User'>

    >>> app = ZopeTestCase.app()
    >>> user = getattr(app, ZopeTestCase.folder_name
    ...                ).acl_users.getUserById(ZopeTestCase.user_name)
    >>> user.getRoles()
    ('test_role_1_', 'Authenticated')
    >>> ZopeTestCase.close(app)

Set up the new layer.

    >>> runner.setup_layer(options, foo_layer, setup_layers)
    Set up FooLayer in ... seconds.

Now the changed made by afterSetUp() are reflected.

    >>> authenticated = SecurityManagement.getSecurityManager(
    ...     ).getUser()
    >>> authenticated
    <User 'test_user_1_'>
    >>> authenticated.getRoles()
    ('Manager', 'Authenticated')

Tear down just the new layer.

    >>> runner.tear_down_unneeded(
    ...     options, [ztc.ztc_layer], setup_layers)
    Tear down FooLayer in ... seconds.

Everything is restored to its previous state.

    >>> SecurityManagement.getSecurityManager().getUser()
    <SpecialUser 'Anonymous User'>

    >>> app = ZopeTestCase.app()
    >>> user = getattr(app, ZopeTestCase.folder_name
    ...                ).acl_users.getUserById(ZopeTestCase.user_name)
    >>> user.getRoles()
    ('test_role_1_', 'Authenticated')
    >>> ZopeTestCase.close(app)

Finish tearing down the rest of the layers.

    >>> runner.tear_down_unneeded(options, [], setup_layers)
    Tear down collective.testcaselayer.ztc.ZTCLayer in ... seconds.
