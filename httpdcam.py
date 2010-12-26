#!/usr/bin/python


#import cgi

from os import curdir, sep, chdir, getcwd, listdir
import socket
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from android import Android


HTWD = '/sdcard/sl4a/scripts/spy'
PORT = 8080

class MyHandler(BaseHTTPRequestHandler):

    def serve_file(self, content='',binary=False):
        if binary:
            f = open(curdir + sep + self.path, 'rb')
        else:
            f = open(curdir + sep + self.path)
        self.send_response(200)
        if content != '':
            self.send_header('Content-type', content)
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
        return
        
    def takePics_1(self):
        #capture_location = '/sdcard/sl4a/scripts/www/image_cam.jpg'
        capture_location = curdir + sep + 'image_cam.jpg'
        droid.cameraCapturePicture(capture_location, True)
        return True

    def do_GET(self):
        try:
            
            if self.path == '/':
                self.path = '/index_.html'
            
            elif self.path == '/image_cam.jpg':
                self.serve_file('image/jpeg', binary=True)
                success = self.takePics_1()
                if success:
                    print "[+] Took a picture successfuly"
                else:
                    print "[-] The shoot FAILED !!"
            
            extf = self.path.split('.')[-1]
            print
            print self.path
            print extf
            print
            
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
            self.send_error(404,'File Not Found: %s' % self.path)

            
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
        global droid
        droid = Android()
        
        server = HTTPServer(('', PORT), MyHandler)
        print '[#] started httpserver on port %d' % PORT
        print '[#] \t\t and local IP : %d' % getIP()
        print '[#] \t\t and external IP : %d' % getIP()
        print
        chdir(HTWD)
        print getcwd()
        print listdir(curdir)
        print curdir
        print sep
        print
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
    finally:
        server.socket.close()

if __name__ == '__main__':
    main()

