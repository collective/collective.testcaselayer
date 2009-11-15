.. -*-doctest-*-

Functional and testbrowser testing patches
==========================================

To use these patches, include the collective.testcaselayer
configure.zcml.  The patches address some bugs in
Testing.ZopeTestCase.

Data streamed to the response
-----------------------------

Due to some behavior in Testing.ZopeTestCase.zopedoctest.functional,
the testbrowser.contents was empty when data had been streamed
directly into the response (as opposed to returning the data from the
callable published).  This made it difficult to do functional testing
for code that needed to stream data to the response for performance,
such as when the response data is very large and would consume too
much memory.

Stream iterators
----------------

A patch taken from plone.app.blob is also included so that HTTP
responses in the test environment support stream iterators.  This
allows functional testing of code that makes use of stream iterators.

HTTP_REFERRER
-------------

Due to `bug #98437 <https://bugs.launchpad.net/bugs/98437>`_,
"TestBrowser Referer: header set to 'localhost'", some testbrowser
requests would raise NotFound.  Two examples would be visiting the
Plone login_form directly rather than following a link, or using the
Plone content_status_history form.    

Test the Patches
----------------

Add a document which renders the referer.

    >>> folder.addDTMLDocument(
    ...     'index_html', file='''\
    ... <html><body>
    ... <dtml-var "REQUEST['HTTP_REFERER']">
    ... <form action="." method="post" id="post"></form>
    ... <form action="." method="get" id="get"></form>
    ... <a href=".">link</a>
    ... </html></body>
    ... ''')
    ''

Open a browser.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> browser.handleErrors = False

Before patching, fresh requests have an invalid referer.

    >>> browser.open(folder.index_html.absolute_url())
    >>> print browser.contents
    <html><body>
    localhost
    <form action="." method="post" id="post"></form>
    <form action="." method="get" id="get"></form>
    <a href=".">link</a>
    </html></body>

Add a script that streams content to the response.

    >>> from Products.PythonScripts import PythonScript
    >>> PythonScript.manage_addPythonScript(folder, 'foo.txt')
    ''
    >>> folder['foo.txt'].ZPythonScript_edit(params='', body='''\
    ... context.REQUEST.response.setHeader('Content-Type', 'text/plain')
    ... context.REQUEST.response.setHeader(
    ...     'Content-Disposition',
    ...     'attachment;filename=foo.txt')
    ... context.REQUEST.response.write('foo')''')

Before patching, data streamed to the response is not in the browser
contents.

    >>> browser.open(folder['foo.txt'].absolute_url())
    >>> browser.isHtml
    False
    >>> print browser.contents

Add a script that returns a stream iterator.

    >>> from Products.PythonScripts import PythonScript
    >>> PythonScript.manage_addPythonScript(folder, 'bar.txt')
    ''
    >>> folder['bar.txt'].ZPythonScript_edit(params='', body='''\
    ... from collective.testcaselayer.testing.iterator import (
    ...     StreamIterator)
    ... context.REQUEST.response.setHeader('Content-Type', 'text/plain')
    ... context.REQUEST.response.setHeader(
    ...     'Content-Disposition',
    ...     'attachment;filename=bar.txt')
    ... return StreamIterator(['bar', 'qux'])''')

    >>> from AccessControl import allow_module
    >>> allow_module('collective.testcaselayer.testing.iterator')

Stream iterators are not supported.

    >>> browser.open(folder['bar.txt'].absolute_url())
    >>> browser.isHtml
    False
    >>> print browser.contents
    ['bar', 'qux']

Apply the patches.

    >>> from Products.Five import zcml
    >>> from Products.Five import fiveconfigure
    >>> from collective import testcaselayer
    >>> fiveconfigure.debug_mode = True
    >>> zcml.load_config('testing.zcml', package=testcaselayer)
    >>> fiveconfigure.debug_mode = False

A fresh request should have no referer.

    >>> browser.open(folder.index_html.absolute_url())
    >>> print browser.contents
    <html><body>
    <form action="." method="post" id="post"></form>
    <form action="." method="get" id="get"></form>
    <a href=".">link</a>
    </html></body>

Submitting a form via post should have no referer.

    >>> browser.getForm('post').submit()
    >>> print browser.contents
    <html><body>
    <form action="." method="post" id="post"></form>
    <form action="." method="get" id="get"></form>
    <a href=".">link</a>
    </html></body>

Submitting a form via get should have no referer.

    >>> browser.getForm('get').submit()
    >>> print browser.contents
    <html><body>
    <form action="." method="post" id="post"></form>
    <form action="." method="get" id="get"></form>
    <a href=".">link</a>
    </html></body>

Clicking a link should set the referer.

    >>> browser.getLink('link').click()
    >>> print browser.contents
    <html><body>
    http://nohost/test_folder_1_/...
    <form action="." method="post" id="post"></form>
    <form action="." method="get" id="get"></form>
    <a href=".">link</a>
    </html></body>

Data streamed to the response is now in the browser contents.

    >>> browser.open(folder['foo.txt'].absolute_url())
    >>> browser.isHtml
    False
    >>> print browser.contents
    Status: 200 OK
    X-Powered-By: Zope (www.zope.org), Python (www.python.org)
    Content-Length: 0
    Content-Type: text/plain
    Content-Disposition: attachment;filename=foo.txt
    foo

Stream iterators are now in the browser contents.

    >>> browser.open(folder['bar.txt'].absolute_url())
    >>> browser.isHtml
    False
    >>> print browser.contents
    barqux
