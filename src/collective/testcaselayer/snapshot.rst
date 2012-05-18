.. -*-doctest-*-

collective.testcaselayer.snapshot
=================================

Snapshot layers build on sandboxed layers but use a real FileStorage
for each layer instead of a DemoStorage.  If present on subsequent
test runs, the FileStorage corresponding to the layer is used instead
of running the layer set up again.  This can be used to greatly
expedite subsequent test runs.  It can also be used get more accurate
profiling or coverage data from the test runner by excluding the code
necessary to set up the layers.

WARNING: DO NOT USE!
--------------------

Successful testing requires consistency.  Snapshot layers can very
easily cause very significant inconsistency.

If code changes would result in changes to the snapshot layer, using
the snapshot will not reflect those changes.  If a snapshot layer
makes changes to anything other than the ZODB, those changes will not
be reproduced when a snapshot is used.

As such, snapshot layers should only be used in the inner loop of the
testing workflow and should never be used for the final testing
verification.  Using snapshot layers inappropriately *will* result in
false positives, bad code, and large losses in productivity.

Using Snapshot Layers
---------------------

Successful use of snapshot layers depends on the following:

  - Only use snapshots for sandbox layers where the layer and *all*
    it's base sandbox layers make changes to the *ZODB only*

  - *Use only* when repeatedly running the specific test your working
    on immediately, the inner loop of your testing workflow

  - Only snapshot layers that work in progress will not affect *at
    all*

  - Run tests *without any* snapshots the moment any unexpected
    results are encountered

  - Always run all tests without any snapshot layers *before
    committing* work in progress

Use of snapshot layers is intentionally manual and should never be
automated so as to avoid the inconsistency that can occur when a
snapshot layer is used unintentionally.  As such, snapshot layers are
used by passing command-line options to the test runner.

The FileStorage files will be named after the layer name as returned
by zope.testing.testrunner.find.name_from_layer().  As such, the
effects of using snapshotted layers whose name is the same are
undefined.  The files will be placed in the directory given in the
fss_dir argument which defaults to '$INSTANCEHOME/var'.
Currently, no implementation for converting storage is provided so the
storages of any base layers must also be FileStorages.

TODO
