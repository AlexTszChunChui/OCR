import zipfile
import pytesseract
import cv2 as cv
import numpy as np
import os
import json
import pickle
import io
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from math import ceil
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# class variable
file = zipfile.ZipFile('readonly/small_img.zip', 'r')
newspaperlst = file.infolist()
img_wordict = dict()
cached = dict()

# build up the dict that mapping the newspaper image and all the word on it
def database():
    global img_wordict
    filepath = ('readonly/wordict.pkl')
    
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            img_wordict = pickle.load(f)
    
    else:
        for news in newspaperlst:
            imgfile = file.open(news.filename)
            img = Image.open(imgfile)
            text = separateword(img)
            img_wordict[text] = news
        with open(filepath, 'wb') as f:
            pickle.dump(img_wordict, f)
    
# OCR function for getting all the word of a image object
def separateword(img):
    img = img.convert('L')
    config = '--psm 3 --oem 1'
    text = pytesseract.image_to_string(img, config=config)
    text = text.replace(' ', '')
    return text.lower()
    
# OCR function for getting all the faces of a image object
def detectfaces(img):
    cv_img_bin=cv.threshold(np.array(img), 170, 255, cv.THRESH_BINARY)[1]
    faces = face_cascade.detectMultiScale(cv_img_bin, 1.45)
    result = list()
    for x,y,w,h in faces:
        result.append(img.crop((x, y, x + w, y + h)))
    return result

# Pasteing all the faces get from detectfaces on a contact_sheet
def concatenate(img_lst):
    sheet_width = 500
    sheet_height = max(1, ceil(len(img_lst) / 5)) * 100
    contact_sheet = Image.new('RGB', (sheet_width, sheet_height), color=(0, 0, 0))
    x = 0
    y = 0
    
    for image in img_lst:
        image.thumbnail((100, 100))
        contact_sheet.paste(image, (x, y))
        x += 100
        if x >= sheet_width:
            x = 0
            y += 100
    
    return contact_sheet

# Finding all the image object that have the string user input
def related(word):
    result = cached.get(word)
    if (result):
        return result
    
    else:
        result = list()
        for k in img_wordict.keys():
            if word in k:
                result.append(img_wordict[k])
        cached[word] = result
        savecached()
        return result

def savecached():
    with open('readonly/cached', 'wb') as f:
            pickle.dump(cached, f)  

# display method, the code was written in Jupytor Notebook environment with Ipython.display method, this is a subtitile version for desktop
def display(img):
    app = QApplication([])
    label = QLabel()
    pixmap = QPixmap.fromImage(ImageQt(img))
    label.setPixmap(pixmap)
    label.show()
    app.exec_()

# The main function that recieve that player input, and call other function for the result
def search(word):
    database()
    word = word.lower()

    if os.path.exists('readonly/cached'):
        with open('readonly/cached', 'rb') as f:
            cached = pickle.load(f)

    img_lst = related(word)
    for news in img_lst:
        print('Result found in file {}'.format(news.filename))
        imgfile = file.open(news.filename)
        img = Image.open(imgfile)
        result = detectfaces(img)
        if result:
            display(concatenate(result))
        else:
            print('But there were no faces in the file!')




