import time
import BaseHTTPServer
from urlparse import urlparse, parse_qs
from selenium import webdriver
from PIL import Image


HOST_NAME = '0.0.0.0'
PORT_NUMBER = 80

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_img(url):
        from selenium import webdriver
        driver = webdriver.PhantomJS()
        driver.set_window_size(1920, 1080)
        driver.get(url)
        driver.save_screenshot('page.jpg')
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
        server = parse_qs(urlparse(s.path).query)
        url = 'http://applemusic.tumblr.com/beats1'
        driver = webdriver.PhantomJS()
        driver.set_window_size(1920, 1080)
        if s.path.startswith('/audio/wat/nowz.jpg'):
            driver.get(url)
            driver.save_screenshot('page.jpg')
            img = Image.open("page.jpg")
            left = 360
            top = 810
            width = 100
            height = 95
            box = (left, top, left+width, top+height)
            img4 = img.crop(box)
            img4.save("img5.jpg")
            f=open("C:\Users\Guilherme\Desktop\img5.jpg", 'rb')
            s.send_response(200)
            s.send_header('Content-type',        'image/jpg')
            s.end_headers()
            s.wfile.write(f.read())
            f.close()
        elif s.path.startswith('/audio/wat/show.jpg'):
            driver.get(url)
            driver.save_screenshot('page.jpg')
            img = Image.open("page.jpg")
            left = 460
            top = 830
            width = 150
            height = 30
            box = (left, top, left+width, top+height)
            img4 = img.crop(box)
            img4.save("img6.jpg")
            f=open("C:\Users\Guilherme\Desktop\img6.jpg", 'rb')
            s.send_response(200)
            s.send_header('Content-type',        'image/jpg')
            s.end_headers()
            s.wfile.write(f.read())
            f.close()
        else:
            s.send_response(404)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write("<html><head><title>Title goes here.</title></head>")
            s.wfile.write("<body><p>This is a test.</p>")
            s.wfile.write("<p>You accessed path: %s</p>" % s.path)
            s.wfile.write("</body>" + str(server) + "</html>")

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
