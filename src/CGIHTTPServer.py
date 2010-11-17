#!/usr/bin/python
"""CGI-savvy HTTP Server.
"""


__version__ = "0.4"

__all__ = ["CGIHTTPRequestHandler"]

import os
import sys
import urllib
import BaseHTTPServer
import SimpleHTTPServer
import select
import cStringIO
import pychain
import cgi
 
worderator = pychain.Worderator()

class CGIHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    """Complete HTTP server with GET, HEAD and POST commands.

    """

    # Make rfile unbuffered -- we need to read one line and then pass
    # the rest to a subprocess, so we can't use buffered input.
    rbufsize = 0

    def do_POST(self):
        """Serve a POST request.
        """
        pos = self.path.find('?')
        if pos:
          qs = cgi.parse_qs(self.path[pos+1:])
        else:
          qs = {}  
        length = qs.get('length', [12])
        num = qs.get('num', [5])
        weightings = {}
        for chain in worderator.listChains():
           if qs.has_key(chain):
             weightings[chain] = int(qs[chain][0])
        output = ""
        print num
        for x in range(0, int(num[0])):
            output += worderator.worderate(length=int(length[0]), weighting=weightings) + "\n"
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", str(len(output)))
        self.end_headers()
        f = cStringIO.StringIO(output)
        self.copyfile(f, self.wfile)
        f.close()


    def do_GET(self):
	"""
        """
        if 1 or self.path.startswith("/do"):
          return self.do_POST()
        else:
          SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

def test(HandlerClass = CGIHTTPRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    SimpleHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()
