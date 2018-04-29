
'''
Blurring Program using convolution technique with OpenCV2

*Revision History*
2018-04-28 Originally written by Chanhaeng

'''
import numpy as np
import cv2
from tkinter import filedialog
from tkinter import *

# IMG Load using file dialog
def ChanIMGload(mode):
    root = Tk()
    root.filename = filedialog.askopenfilename()
    if not root.filename:
        print("Error! You didn't specify file name for load")
        root.destroy()
        return None
    
    print("Loading ", root.filename, " . . .")
    IMG = cv2.imread(root.filename, mode)
    root.destroy()
    return IMG

# IMG Save using file dialog
def ChanIMGSave(IMG):
    root = Tk()
    root.filename = filedialog.asksaveasfilename(title="Save a file", defaultextension='.jpg.',
                                                filetypes=[('image files', ('.jpg'))])
    if not root.filename:
        print("Error! You didn't specify file name for save")
        root.destroy()
        return None

    check = cv2.imwrite(root.filename, IMG)
    if check is True:
        print("Image Save Done! ", root.filename)
    else:
        print("Fail to save the image ", root.filename)
    root.destroy()
    return check
    

# in order to pass Null function on createTrackbar()
def nothing(x): 
    pass

RADIUS = 3.14 * 2
MASK_SIZE = 5
ChanBlurMask = np.ones((MASK_SIZE,MASK_SIZE),np.float32) / (MASK_SIZE * MASK_SIZE)

# Main facility of this program
def chanBlur(event, x, y, flags, userdata):
    global InputImage
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if InputImage is not None:
            for radiusY in range(int(y - RADIUS), int(y + RADIUS)):
                for radiusX in range(int(x - RADIUS), int(x + RADIUS)):
                    b = 0
                    g = 0
                    r = 0
                    for checkY, my in zip(range(radiusY- int(MASK_SIZE/2), radiusY + int(MASK_SIZE/2) + 1), range(MASK_SIZE)):
                        for checkX, mx in zip(range(radiusX - int(MASK_SIZE/2), radiusX + int(MASK_SIZE/2) + 1), range(MASK_SIZE)):
                            b += InputImage[checkY,checkX,0] * ChanBlurMask[my,mx]
                            g += InputImage[checkY,checkX,1] * ChanBlurMask[my,mx]
                            r += InputImage[checkY,checkX,2] * ChanBlurMask[my,mx]
                    if b > 255 : b = 255
                    elif b < 0: b = 0
                    if g > 255 : g = 255
                    elif g < 0: g = 0
                    if r > 255 : r = 255
                    elif r < 0: r = 0
                    
                    InputImage[radiusY,radiusX] = np.uint8([b,g,r])


# make Window
CV_WINDOW_NAME = "Chan Test"

cv2.namedWindow(CV_WINDOW_NAME, cv2.WINDOW_NORMAL)

# In order to use the defined length of trackbar in Window.
desiredWidth = 640
desiredHeight = 480
cv2.resizeWindow(CV_WINDOW_NAME, desiredWidth, desiredHeight)

# make Trackbars for loading and saving a image.
switch1 = "1 : Load"
switch2 = "1 : Save"
cv2.createTrackbar(switch1, CV_WINDOW_NAME, 0, 1, nothing)
cv2.createTrackbar(switch2, CV_WINDOW_NAME, 0, 1, nothing)

# Setup before main loop

InputImage = None # the resource image a user want to blur
isShow = False # Main boolean variable to show a image, related to InputImage
cv2.setMouseCallback(CV_WINDOW_NAME, chanBlur, InputImage)  # Set mouse function. A user can blur a image with a mouse button click

# Main Loop
while  True :   
    if cv2.waitKey(1) & 0xFF == 27: # ESC KEY
        break
    if cv2.getWindowProperty(CV_WINDOW_NAME, 0) < 0: # WINDOW EXIT BUTTON
        break
    
    load = cv2.getTrackbarPos(switch1, CV_WINDOW_NAME)
    save = cv2.getTrackbarPos(switch2, CV_WINDOW_NAME)

    if load == 1: # If a user wants to load a image
        cv2.setTrackbarPos(switch1, CV_WINDOW_NAME, 0)
        InputImage = ChanIMGload(1)
        # Error Handling
        if InputImage is None:
            print("Please Load a image Again")
            isShow = False
        else:
            isShow = True
        
    if save == 1: # If a user wants to save an image
        cv2.setTrackbarPos(switch2, CV_WINDOW_NAME, 0)

        # Error Handling
        if isShow == False:
            print("Load your Image Before Save")
        else:
            check = ChanIMGSave(InputImage)
            if check == False or check == None:
                print("Please Save your Image Again")

    # Show an image only when the InputImage variable has an exact data.
    if isShow == True:
        cv2.imshow(CV_WINDOW_NAME, InputImage)
    
cv2.destroyAllWindows()
