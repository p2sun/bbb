from selenium import webdriver
import os, time
from PIL import Image
from math import sqrt
from skimage.feature import blob_dog, blob_log
from skimage.color import rgb2gray
import numpy as np



DRIVER_BIN = os.path.join("/usr/local/share", "chromedriver")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

def get_screen():
    browser = webdriver.Chrome(executable_path = DRIVER_BIN, chrome_options=options)
    browser.get('http://codebb.cloudapp.net/BaseInvaders.html')
    time.sleep(5)
    element = browser.find_element_by_css_selector("#gameCanvas")
    location = element.location
    size = element.size
    browser.save_screenshot('screenie.png')
    browser.quit()
    return location,size

def crop_image(location,size):
    img = Image.open("screenie.png")
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = img.crop((left, top, right, bottom)) # defines crop points
    im.save('screenshot.png') # saves new cropped image

def get_areas_interest():
    img_arr = np.array(Image.open('screenshot.png'), dtype=np.uint8)
    image_gray = rgb2gray(img_arr)

    # get mines
    mine_blobs = blob_log(image_gray, max_sigma=30, num_sigma=10, threshold=.05)
    mine_blobs[:, 2] = mine_blobs[:, 2] * sqrt(2)
    mines = mine_blobs[(mine_blobs[:,2] > 5.5) & (mine_blobs[:,2] < 7)]

     # get worm holes
    blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.3)
    blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)
    worm_holes = blobs_dog[(blobs_dog[:,2] > 12)]

    return mines, worm_holes

def pipeline():
    mines = []
    worm_holes = []

    location,size = get_screen()
    crop_image(location,size)

    mines, worm_holes = get_areas_interest()
    print mines
    print worm_holes

pipeline()
