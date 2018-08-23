from Tkinter import *
from PIL import Image, ImageTk
import tkFileDialog
import numpy as np
import UtilityFunctions as UF
import cv2
import unicodedata
import tkMessageBox

__author__ = 'Gilad Gecht & Anton Vasserman'


root = Tk()
root.title('Fisheye')
root.geometry('600x670')
root.resizable(width=False,height=False)
root.iconbitmap('FishIcon.ico')

img = [None]
tkimg = [None]
tkimg[0] = ImageTk.PhotoImage(Image.open('fish_eye.png').resize((600, 600), Image.ANTIALIAS))
param = [0]
tkimgTemp = [None] * 21 # Reference Array to store the images,
cvimgTemp = [None] * 21 # to avoid the image being deleted by the garbage collector


# Save image to desktop function
def mySaveImage():
    if img[0] != None:
        #filename = tkFileDialog.asksaveasfilename(filetypes=[('JPEG', '*.jpg')])#, ('All files', '*')])
        filename = tkFileDialog.asksaveasfilename(filetypes=[('All files', '*')])
        if filename:
            #cv2.imwrite(filename + '.jpg', cvimgTemp[param[0] + 10])
            cv2.imwrite(filename, cvimgTemp[param[0] + 10])

# Load a desired image
def myLoadImage():
    dlg = tkFileDialog.Open(filetypes = [('image files', '*.jpg'), ('All files', '*')])
    fl = dlg.show()
    if fl != '':
        print fl
        imageCanvas.delete('all')
        fls = unicodedata.normalize('NFKD', fl).encode('ascii', 'ignore')
        img[0] = Image.open(fl)
        img[0] = img[0].resize((600, 600), Image.ANTIALIAS)
        tkimg[0] = ImageTk.PhotoImage(img[0])
        imageCanvas.create_image((0, 0), anchor = NW, image = tkimg[0])
        for i in range(21): # Number of distortion pictures created
            par = np.float64(i - 10) / 10
            tempImage = UF.myDistort(fls, par)
            tempImage = tempImage[:, :, ::-1]
            tempFileName = 'tempFile.jpg'
            cv2.imwrite(tempFileName, tempImage)
            cvimgTemp[i] = tempImage.copy()

            imgTemp = Image.open(tempFileName)
            imgTemp = imgTemp.resize((600, 600), Image.ANTIALIAS)
            tkimgTemp[i] = ImageTk.PhotoImage(imgTemp)
            print 'Finished image with param: ' + str(par)
        UF.os.remove('tempFile.jpg')
        tkMessageBox.showinfo('Loading Image Process','Loading Cache Memory: \n STATUS - DONE')

# Function to scroll up through the saved distorted images
def upParam():
    if(param[0] < 10) and img[0] != None:
        param[0] = param[0] + 1
        imageCanvas.delete('all')
        imageCanvas.create_image((0, 0), anchor=NW, image=tkimgTemp[param[0] + 10])

# Function to scroll down through the saved distorted images
def downParam(p = param):
    if (param[0] > -10) and img[0] != None:
        param[0] = param[0] - 1
        imageCanvas.delete('all')
        imageCanvas.create_image((0, 0), anchor=NW, image=tkimgTemp[param[0] + 10])

# GUI visualization


LoadIcon = ImageTk.PhotoImage(file = 'LoadIcon.png')
SaveIcon = ImageTk.PhotoImage(file = 'SaveIcon.png')
UpIcon = ImageTk.PhotoImage(file = 'UpIcon.png')
DownIcon = ImageTk.PhotoImage(file = 'DownIcon.png')

buttonLoad = Button(root, image = LoadIcon, height = 52, width = 212, command = myLoadImage)
buttonSave = Button(root, image = SaveIcon, height = 52, width = 212, command = mySaveImage)
buttonUp = Button(root, image = UpIcon, height = 23, width = 100, command = upParam)
buttonDown = Button(root, image = DownIcon, height = 23, width = 100, command = downParam)
imageCanvas = Canvas(root, width = 586, height = 593, borderwidth = 1, relief = 'solid')

imageCanvas.grid(row = 0, column = 0, columnspan = 4, padx = 4, pady = 4)
buttonLoad.grid(row = 1, column = 0, rowspan = 2)
buttonSave.grid(row = 1, column = 1, rowspan = 2)
buttonUp.grid(row = 1, column = 2)
buttonDown.grid(row = 2, column = 2)

imageCanvas.create_image(0, 0, anchor = NW, image = tkimg[0])

root.mainloop()