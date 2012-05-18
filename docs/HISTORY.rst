Changelog
=========

1.5 - 2012-05-18
----------------

* Plone 4.1 compatibility.
  [rossp]

* Let layer tear down do cleanup.  Allows post_mortem debugging to see
  the state in the TB before DB connections are closed or other
  cleanup is done.
  [rossp]

1.4 - 2011-07-15
----------------

* Move the mock mail host to an actual GS profile so it won't be
  replaced when dependent layers run their own profiles.  Also makes
  the mock mail host usable outside of tests.
  [rossp]

* Add some utility methods for setting testbrowser AT calendar widgets
  without end/beginning-of-month intermittent failures.
  [rossp]

* Avoid a version conflict between PloneTestCase and
  zope.testing/testrunner.
  [rossp]

1.3 - 2010-02-09
------------------

* Add a loadZCML convenience method [rossp]

* Add a common layer with some useful test setup [rossp]

* Add a mock mail host layer [rossp]

1.2.2 - 2009-11-14
------------------

* Add functional testing support for stream iterator responses.  Taken
  from witsch's plone.app.blob testing patches.
  [rossp]

* Zope 2.10-2.12 compatibility
  [rossp, witsch]

* Fix `Sandboxed` replacement for Zope 2.12 / Plone 4.
  [witsch]

1.2.1 - 2009-10-11
------------------

* Move the ZTC functional doctest monkey patches to testing.zcml so
  that they don't get picked up under auto-include.  optilude reported
  this was breaking debug-mode.

1.2 - 2009-08-21
----------------

* Add a patch so that data streamed to the response is available in
  testbrowser.contents. [rossp]
* Add a patch for the HTTP_REFERER testbrowser bug.
  https://bugs.launchpad.net/bugs/98437 [rossp]

1.1 - 2009-07-29
----------------

* Fix release.  Files were missing due to the setuptools interaction
  with SVN 1.6.

1.0 - 2009-07-29
----------------

* Tested against Plone 3.3rc4

* Add sample code for basic Plone test case layers

* Deprecate zope.testing<3.6 support

* The collective.testcaselayer.ptc module needs to call
  ptc.setupPloneSite() in order to make sure the plone site exists

0.2 - 2008-01-08
----------------

* Make the self.folder attribute available in PortalTestCase
  sub-layers
* Make tests compatible with zope.testing.testrunner refactoring

0.1 - 2008-05-23
----------------

* Initial release

