import sys
import transaction

from Testing.ZopeTestCase.functional import savestate
from Testing.ZopeTestCase.zopedoctest import functional

orig_outstream_init = functional.DocResponseWrapper.__init__
def outstream_init(self, response, outstream, path, header_output):
    if not response.body:
        response.body = outstream.getvalue()
    orig_outstream_init(self, response, outstream, path,
                        header_output)

@savestate
def http(request_string, handle_errors=True):
    """Execute an HTTP request string via the publisher

    This is used for HTTP doc tests.
    """
    import urllib
    import rfc822
    from cStringIO import StringIO
    from ZPublisher.Response import Response
    from ZPublisher.Test import publish_module

    # Commit work done by previous python code.
    transaction.commit()

    # Discard leading white space to make call layout simpler
    request_string = request_string.lstrip()

    # Split off and parse the command line
    l = request_string.find('\n')
    command_line = request_string[:l].rstrip()
    request_string = request_string[l+1:]
    method, path, protocol = command_line.split()
    path = urllib.unquote(path)

    instream = StringIO(request_string)

    env = {"HTTP_HOST": 'localhost',
           "REQUEST_METHOD": method,
           "SERVER_PROTOCOL": protocol,
           }

    p = path.split('?')
    if len(p) == 1:
        env['PATH_INFO'] = p[0]
    elif len(p) == 2:
        [env['PATH_INFO'], env['QUERY_STRING']] = p
    else:
        raise TypeError, ''

    header_output = functional.HTTPHeaderOutput(
        protocol, ('x-content-type-warning', 'x-powered-by',
                   'bobo-exception-type', 'bobo-exception-file',
                   'bobo-exception-value', 'bobo-exception-line'))

    headers = [functional.split_header(header)
               for header in rfc822.Message(instream).headers]

    # Store request body without headers
    instream = StringIO(instream.read())

    for name, value in headers:
        name = ('_'.join(name.upper().split('-')))
        if name not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            name = 'HTTP_' + name
        env[name] = value.rstrip()

    if env.has_key('HTTP_AUTHORIZATION'):
        env['HTTP_AUTHORIZATION'] = functional.auth_header(
            env['HTTP_AUTHORIZATION'])

    outstream = StringIO()
    response = Response(stdout=outstream, stderr=sys.stderr)

    publish_module('Zope2',
                   response=response,
                   stdin=instream,
                   environ=env,
                   debug=not handle_errors,
                  )
    header_output.setResponseStatus(response.getStatus(), response.errmsg)
    header_output.setResponseHeaders(response.headers)
    header_output.appendResponseHeaders(response._cookie_list())
    header_output.appendResponseHeaders(response.accumulated_headers.splitlines())

    functional.sync()

    return functional.DocResponseWrapper(response, outstream, path, header_output)
