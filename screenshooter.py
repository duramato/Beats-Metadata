import time
import os
import logging as logger
from selenium import webdriver
starttime=time.time()
logger.basicConfig(filename='screenshooter.log',level=logger.DEBUG)
url = 'http://applemusic.tumblr.com/beats1'
while True:
    #driver = webdriver.PhantomJS()
    #driver.set_window_size(1920, 1080)
    #driver.get(url)
    #driver.save_screenshot('page.jpg')
    try:
        print('hey')
    except Exception:
        logger.info('No File exsits')
    logger.info('screenie init')
    os.system("./webshots --width 1080 --height 1920 https://twitter.com/radio_scrobble")
    os.system("mv twitter.com-radio_scrobble.1080x1920.png music_page.png")
    #print('Screenie taken @ ' + str(time.time()) )
    logger.info('Screenie taken')
    time.sleep(10.0 - ((time.time() - starttime) % 10.0))
