import json
import sys
import BaseHTTPServer
import httplib
import traceback
import socket
from BaseHTTPServer import BaseHTTPRequestHandler

shopPort = 80


def sendAndVerify(ip, port, uri):
    print "start to invoke %s" % uri
    httpClient = None
    try:
        httpClient = httplib.HTTPConnection(ip, port, timeout=30)
        headers = {"Content-type": "application/x-www-form-urlencoded"
            , "Accept": "text/plain"}
        httpClient.request("GET", uri, None, headers);
        response = httpClient.getresponse()
        retStatus = response.status
        if retStatus != 200:
            print "Test fail, status code is %s" % retStatus
            return bool('False')
        return bool('True')
    except Exception, e:
        print "Test fail, status exception is %s" % e
        traceback.print_exc()
        return bool('False')
    finally:
        if httpClient:
            httpClient.close()


def getLocalIP():
    return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]


class TodoHandler(BaseHTTPRequestHandler):
    localIP = getLocalIP()

    def do_GET(self):
        if self.path == '/api/v6/promotion/query':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('localIP', self.localIP)
            self.end_headers()
            msg = {
                "promotions":
                    [{"itemId":"001", "status":"off"},
                          {"itemId":"002", "status":"on"},
                          {"itemId":"003", "status":"on"}
                          ]
                   }
            self.wfile.write(json.dumps(msg))
        elif self.path == '/api/v6/promotion/item/discount':
            if sendAndVerify("shop", shopPort, "/api/v6/product/deliver"):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('localIP', self.localIP)
                self.end_headers()
                msg = {
                    "discount": "40",
                    "itemId": "002"
                }
                self.wfile.write(json.dumps(msg))
            else:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                msg = {"exception":"Error invoke %s" % "/api/v6/product/deliver"}
                self.wfile.write(json.dumps(msg))
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            msg = {
                "status":"UP"
            }
            self.wfile.write(json.dumps(msg))
        else:
            self.send_error(404, "{\"message\":\"File %s not found.\"}" % self.path)
            return


if __name__ == '__main__':
    # Start a simple server, and loop forever
    ServerClass  = BaseHTTPServer.HTTPServer
    hostPort = int(sys.argv[1])
    print "host port is %s"%hostPort
    server = ServerClass(('0.0.0.0', hostPort), TodoHandler)
    print "Starting promotionService, use <Ctrl-C> to stop"
    server.serve_forever()