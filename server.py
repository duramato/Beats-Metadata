import time
import BaseHTTPServer
from urlparse import urlparse, parse_qs
from selenium import webdriver
import PIL
from PIL import Image


HOST_NAME = '0.0.0.0'
PORT_NUMBER = 80

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_img(url):
        from PIL import Image
        img = Image.open("page.jpg")
        left = 350
        top = 810
        width = 500
        height = 95
        box = (left, top, left+width, top+height)
        img4 = img.crop(box)
        img4.save("img5.jpg")
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        if s.path.startswith('/audio/wat/showimg.jpg'):
            server = parse_qs(urlparse(s.path).query)
            img = Image.open("page.jpg")
            left = 360
            top = 810
            width = 100
            height = 95
            box = (left, top, left+width, top+height)
            img4 = img.crop(box)
            img4.save("img5.jpg")
            f=open("img5.jpg", 'rb')
            s.send_response(200)
            s.send_header('Content-type',        'image/jpg')
            s.end_headers()
            s.wfile.write(f.read())
            f.close()
        elif s.path.startswith('/audio/wat/show.jpg'):
            server = parse_qs(urlparse(s.path).query)
            img = Image.open("page.jpg")
            left = 460
            top = 830
            width = 150
            height = 30
            box = (left, top, left+width, top+height)
            img4 = img.crop(box)
            img4.save("img6.jpg")
            f=open("img6.jpg", 'rb')
            s.send_response(200)
            s.send_header('Content-type',        'image/jpg')
            s.end_headers()
            s.wfile.write(f.read())
            f.close()
        elif s.path.startswith('/audio/wat/art.jpg'):
            server = parse_qs(urlparse(s.path).query)
            img = Image.open("twitter.com-radio_scrobble.1080x1920.png")
            left = 470
            top = 580
            width = 500
            height = 500
            box = (left, top, left+width, top+height)
            img4 = img.crop(box)
            img4.save("cover.jpg")
            f=open("cover.jpg", 'rb')
            s.send_response(200)
            s.send_header('Content-type',        'image/jpg')
            s.end_headers()
            s.wfile.write(f.read())
            f.close()
        elif s.path.startswith('/audio/wat/nowz.jpg'):
            server = parse_qs(urlparse(s.path).query)
            img = Image.open("twitter.com-radio_scrobble.1080x1920.png")
            left = 460
            top = 470
            width = 520
            height = 100
            box = (left, top, left+width, top+height)
            img4 = img.crop(box)
            img4.save("now1.jpg")
            
            basewidth = 375
            img = Image.open('now1.jpg')
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
            img.save('now.jpg')
            
            f=open("now.jpg", 'rb')
            s.send_response(200)
            s.send_header('Content-type',        'image/jpg')
            s.end_headers()
            s.wfile.write(f.read())
            f.close()
        else:
            f=open("page.jpg", 'rb')
            s.send_response(404)
            s.send_header('Content-type',        'image/jpg')
            s.end_headers()
            s.wfile.write(f.read())
            f.close()

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
