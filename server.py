import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer, test as _test
from SocketServer import ThreadingMixIn
import BaseHTTPServer
from urlparse import urlparse, parse_qs
from selenium import webdriver
import numpy as np
import PIL
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


HOST_NAME = '0.0.0.0'
PORT_NUMBER = 80


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class SlowHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        if s.path.startswith('/audio/wat/showimg.jpg'):
            from urllib import urlopen
            import json
            import time
            sock = urlopen("http://fuse-music.herokuapp.com/api/programs")
            htmlSource = sock.read()
            sock.close() 
            url = htmlSource
            artists = json.loads(url)
            items = artists.get('programs')
            result = []
            for artist in items:
                title = artist.get("title")
                image = artist.get("image")
                if not image:
                    image = "http://applesocial.s3.amazonaws.com/assets/images/branding/on-air-default.jpg"
                start = int(artist.get("start"))
                time_now = int(time.time())
                start = str(start)[:-3]
                end = int(artist.get("end"))
                end = str(end)[:-3]
                if int(end) < int(time_now):
                    #print('Skipping already aired: ' + title)
                    continue
                item = {
                        'title': title,
                        'start': start,
                        'end': end,
                        'now': time_now,
                        'image': image}
                result.append(item)
                #print(item)
            result.sort(key=lambda k: k['start'])
            image = result[0]['image']
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write('<img src="%s">' % image)
            #sourceimg = '<img src="{0}">'.format(image)
            #print(sourceimg)
            #s.wfile.write(sourceimg)
        elif s.path.startswith('/audio/wat/show.jpg'):
            #server = parse_qs(urlparse(s.path).query)
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
            #server = parse_qs(urlparse(s.path).query)
            try:
                img = Image.open("music_page.png")
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
            except IOError:
                print("Ups on cover.jpg")
                f=open("cover.jpg", 'rb')
                s.send_response(200)
                s.send_header('Content-type',        'image/jpg')
                s.end_headers()
                s.wfile.write(f.read())
                f.close()
        elif s.path.startswith('/audio/wat/nowz.jpg'):
            #server = parse_qs(urlparse(s.path).query)
            try:
                img = Image.open("music_page.png")
                left = 460
                top = 470
                width = 520
                height = 100
                box = (left, top, left+width, top+height)
                img4 = img.crop(box)
                #img4.save("now1.jpg")
                
            
                #img = Image.open(sys.argv[1])
                img = img4.convert("RGBA")

                pixdata = img.load()

                # Remove the blue color

                #for y in xrange(img.size[1]):
                #   for x in xrange(img.size[0]):
                #        if pixdata[x, y] == (0, 132, 180, 255):
                #            pixdata[x, y] = (255, 255, 255, 0)
                            
                # Remove the white background

                for y in xrange(img.size[1]):
                   for x in xrange(img.size[0]):
                        if pixdata[x, y] == (255, 255, 255, 255):
                            pixdata[x, y] = (255, 255, 255, 255)
            
                img4 = img
            
            
                basewidth = 375
                img = img4 #Image.open('now1.jpg')
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
                img.save('now.png')
            
                f=open("now.png", 'rb')
                s.send_response(200)
                s.send_header('Content-type',        'image/png')
                s.end_headers()
                s.wfile.write(f.read())
                f.close()
            except IOError:
                print("Ups on now.jpg")
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


def test(HandlerClass = SlowHandler,
         ServerClass = ThreadedHTTPServer):
    _test(HandlerClass, ServerClass)
     
    
if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), SlowHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
