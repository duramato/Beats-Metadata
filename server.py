import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer, test as _test
from SocketServer import ThreadingMixIn
import BaseHTTPServer
from urlparse import urlparse, parse_qs
from selenium import webdriver
import numpy as np
import PIL
import re
from PIL import Image
from PIL import ImageFile
import threading
import urllib
import urllib2
from urllib import urlopen
from urlparse import urlparse, urljoin
import json
import time
import os
import csv
import image2text
ImageFile.LOAD_TRUNCATED_IMAGES = True

title_regex = re.compile(r'(?:(?:https?:)?\/\/.*\/(?:images|uploads)?\/(?:.*\/)?)(.*)', re.I)
HOST_NAME = '0.0.0.0'
PORT_NUMBER = 82

class TumblerGetter():
    @staticmethod
    def ReadCSVasDict(csv_file):
        try:
            with open(csv_file) as csvfile:
                reader = csv.DictReader(csvfile)
                final_result = []
                items = []
                for row in reader:
                    item = {}
                    item = {
                            'title': row['title'],
                            'start': row['start'],
                            'end': row['end'],
                            'now': row['now'],
                            'image': row['image'],
                            'file_name': row['file_name']
                            }
                    items.append(item)
                final_result += items
        except IOError as (errno, strerror):
                print("I/O error({0}): {1}".format(errno, strerror))    
        return final_result
    @staticmethod        
    def WriteDictToCSV(csv_file,csv_columns,dict_data):
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in dict_data:
                    writer.writerow(data.encode("utf8"))
        except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))    
        return   
    @staticmethod
    def BootStrap():
            sock = urlopen("http://fuse-music.herokuapp.com/api/programs")
            htmlSource = sock.read()
            sock.close() 
            url = htmlSource
            artists = json.loads(url)
            dict = artists.get('programs')
            final_result = []
            items = []
            for artist in dict:
                title = artist.get("title")
                image = artist.get("image")
                if not image:
                    image = "https://applesocial.s3.amazonaws.com/assets/images/branding/on-air-default.jpg"
                start = int(artist.get("start"))
                time_now = int(time.time())
                start = str(start)[:-3]
                end = int(artist.get("end"))
                end = str(end)[:-3]
                if int(end) < int(time_now):
                    #print('Skipping already aired: ' + title)
                    continue
                file_name = title_regex.search(image).group(1)
                print('Found "image": {0}'.format(image))
                print('Found "file_name": {0}'.format(file_name))
                if not os.path.isfile(file_name):
                    print("Writting {0} to disk".format(file_name))
                    f = open(file_name,'wb')
                    image_path = urlparse(image)
                    image = "http://" + image_path.netloc + image_path.path
                    print('Found "image": {0}'.format(image))
                    request = urllib2.Request(image)
                    request.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
                    f.write(urllib2.urlopen(request).read())
                    #except Exception as ex:
                        #print("Ups failed retriving image with {0}, retrying...".format(ex))
                        #f.write(urllib.urlopen(image).read())
                    f.close()
                item = {}
                item = {
                        'title': title,
                        'start': start,
                        'end': end,
                        'now': time_now,
                        'image': image,
                        'file_name': file_name
                        }
                items.append(item)
            final_result += items
            import csv
            my_dict = final_result
            csv_columns = ['file_name', 'title','start','end','now','image']
            csv_file = "db.csv"

            TumblerGetter.WriteDictToCSV(csv_file,csv_columns,my_dict)

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
        
            csv_file = "db.csv"
            string = TumblerGetter.ReadCSVasDict(csv_file)
            
            # Create show name image
            image2text.main(string[0]["title"])
            
            f=open(string[0]["file_name"], 'rb')
            s.send_response(200)
            s.send_header('Content-type',        'image/png')
            s.end_headers()
            s.wfile.write(f.read())
            f.close()
            
        elif s.path.startswith('/audio/wat/show.jpg'):
        
            f=open("show.png", 'rb')
            s.send_response(200)
            s.send_header('Content-type',        'image/png')
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
    import threading
    def UpdateJSON():
        print("Updating JSON to CSV")
        TumblerGetter.BootStrap()
        threading.Timer(60, UpdateJSON).start()
        print("Updated JSON to CSV")
    UpdateJSON()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
