.. -*-doctest-*-

========================
collective.testcaselayer
========================

The support for layers provided by zope.testing helps to lessen the
amount of time consumed during test driven development by sharing
expensive test fixtures, such as is often requires for functional
test.  This package provides several well tested facilities to make
writing and using layers faster and easier.

The collective.testcaselayer.common.common_layer, used in the Quick
Start, also includes some commonly useful test fixtures:

    - a mock mail host
    - remove 'Unauthorized' and 'NotFound' from error_log ignored
      exceptions
    - puts the resources registries in debug mode
      (portal_css, portal_javascripts, portal_kss)
