#!/usr/bin/python

import os
import SimpleHTTPServer
import SocketServer
import sys

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print "Port defaulted to 8000"
		port = 8000
	else:
		port = int(sys.argv[1])

	os.chdir("output")

	handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer(("", port), handler)

	print "Serving at port {0}".format(port)
	httpd.serve_forever()