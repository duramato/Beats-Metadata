import time
from selenium import webdriver
starttime=time.time()
url = 'http://applemusic.tumblr.com/beats1'
while True:
    driver = webdriver.PhantomJS()
    driver.set_window_size(1920, 1080)
    driver.get(url)
    driver.save_screenshot('page.jpg')
    print('Screenie taken @ ' + str(time.time()) )
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
