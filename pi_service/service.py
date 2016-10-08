import random
import string
import sys, getopt
import socket

import cherrypy

USAGE = 'service.py -i <local ip address> -p <port>'
DEFAULT_PORT = '8080'

@cherrypy.expose
class StringGeneratorWebService(object):
    
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['mystring']
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string

    def POST(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string

    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string
    
    def DELETE(self):
        cherrypy.session.pop('mystring', None)

def getDefaultHost():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    ip = s.getsockname()[0]
    port = DEFAULT_PORT
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:p:',["ip=","port="])
    except getopt.GetoptError:
        print USAGE 
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print USAGE
        elif opt in ("-i"):
            ip = arg
        elif opt in ("-p"):
            port = int(arg)

    return ip, port

def main():
    ip, port = getDefaultHost()

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
   
    cherrypy.server.socket_host = ip
    cherrypy.server.socket_port = port
    cherrypy.quickstart(StringGeneratorWebService(), '/', conf)

if __name__ == '__main__':
    main() 
