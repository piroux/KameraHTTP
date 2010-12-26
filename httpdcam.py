#!/usr/bin/python
#-*- encoding: utf8 -*-

import os
import socket
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

try:
    from android import Android
except ImportError:
    onPC = True
else:
    onPC = False

if onPC:
    HTWD = '/home/pierre/dev/python/web/one'
else:
    HTWD = '/sdcard/sl4a/scripts/spy'

PORT = 8080

class MyHandler(BaseHTTPRequestHandler):

    def serve_file(self, content=None,binary=False):
        try:
            if binary:
                f = open(os.curdir + self.path, 'rb')
            else:
                f = open(os.curdir + self.path)

            
            try:
                self.send_response(200)
                if content:
                    self.send_header('Content-type', content)
                self.end_headers()
                self.wfile.write(f.read())
                #f.close()
                print "done : %s" % self.path
                return
            finally:
                f.close()
        except IOError, error:
            print "serving the file failed %s : %s" % (self.path, str(error))
            return False
        except NameError, error:
            print "serving the file failed %s : %s" % (self.path, str(error))
            return False

    def takePics_1(self):
        try:
            #capture_location = '/sdcard/sl4a/scripts/www/image_cam.jpg'
            capture_location = HTWD + os.sep + 'image_cam.jpg'
            print capture_location
            droid.cameraCapturePicture(capture_location, True)
            return True
        except IOError, error:
            print "[-] takePics_1 failed : %s" % str(error)
            return False
        except NameError, error:
            print "[-] takePics_1 failed : %s" % str(error)
            return False

    def do_GET(self):
        try:
            if self.path == '/':
                print
                self.path = '/index_.html'

            elif self.path == '/image_cam.jpg':
                self.serve_file('image/jpeg', binary=True)
                success = self.takePics_1()
                if success:
                    print "[+] Took a picture successfully"
                else:
                    print "[-] The shoot FAILED !!"
                return

            extf = self.path.split('.')[-1]
            
            #print
            #print self.path
            #print os.curdir
            #print os.sep
            #print extf
            #print
            
            if extf in ['css', 'csv', 'html', 'plain', 'xml']:
                self.serve_file('text/'+extf)
                
            elif extf == ['js', 'java', 'javascript']:
                self.serve_file('application/javascript')

            elif extf in ['jpeg', 'jpg']:
                self.serve_file('image/jpeg', binary=True)
                
            elif extf in ['png', 'gif', 'bmp', 'tiff']:
                self.serve_file('image/'+extf, binary=True)

            elif extf in ['svg']:
                self.serve_file('image/svg+xml', binary=True)

            else:
                self.serve_file()
                
        except IOError:
            self.send_error(405,'File Not Found: %s' % self.path)


def getIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("google.com", 80))
        IP = s.getsockname()
        return s.getsockname()[0]
    finally:
        s.close()

def main():
    try:
        if not onPC:
            global droid
            droid = Android()
        
        server = HTTPServer(('', PORT), MyHandler)
        
        print
        print "[#] Kamera-server"
        print
        print "[#] HTTPServer started on port %d" % PORT
        print "[#] \tand local IP : %s" % getIP()
        #print "[#] \tand (external)?? IP : %s" % getIP()
        print
        
        os.chdir(HTWD)
        
        print "[#] Listing of the current directory : \n\t%s" % os.getcwd()+os.sep
        for i in os.listdir(os.curdir):
            print "\t\t* %s" % i
            
        print
        server.serve_forever()
        
    except KeyboardInterrupt:
        print '^C received, shutting down server'
    finally:
        server.socket.close()

if __name__ == '__main__':
    main()
    
