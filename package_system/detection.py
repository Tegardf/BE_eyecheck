import cv2
import numpy as np

from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny

def removeFlare(imgBGR):
    lab = cv2.cvtColor(imgBGR,cv2.COLOR_BGR2LAB)
    labPlane = list(cv2.split(lab))
    clahe = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(13,13))
    labPlane[0]=clahe.apply(labPlane[0])
    lab = cv2.merge(labPlane)
    claheBgr=cv2.cvtColor(lab,cv2.COLOR_LAB2BGR)
    grayimg = cv2.cvtColor(claheBgr,cv2.COLOR_BGR2GRAY)
    mask = cv2.threshold(grayimg, 200,255, cv2.THRESH_BINARY)[1]
    result= cv2.inpaint(imgBGR,mask,0.1,cv2.INPAINT_NS)
    return result

def claheFilterContrast(imgBGR):
    lab = cv2.cvtColor(imgBGR,cv2.COLOR_BGR2LAB)
    labPlane=list(cv2.split(lab))
    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(5,5))
    labPlane[0]=clahe.apply(labPlane[0])
    lab = cv2.merge(labPlane)
    claheBgr=cv2.cvtColor(lab,cv2.COLOR_LAB2BGR)
    claheBgr=cv2.GaussianBlur(claheBgr,(5,5),0)
    return claheBgr

def ROI_segmentation(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(gray , (5,5), 0)
    kernelSharp = np.array([[0, -1, 0],[-1,5,-1],[0,-1,0]])
    imgBlur = cv2.filter2D(imgBlur, -1, kernelSharp)
    centerImg = [np.shape(img)[0]/2,np.shape(img)[1]/2]
    circles = cv2.HoughCircles(imgBlur, cv2.HOUGH_GRADIENT, 1, 90, param1 = 235, param2 = 4, minRadius = np.uint64(np.shape(img)[0]/3.5), maxRadius= np.uint64(np.shape(img)[0]/2.8))
    inner_circle = np.around(circles[0][0]).tolist()
    distPoint = [abs(centerImg[0]-inner_circle[0]),abs(centerImg[1]-inner_circle[1])]
    for c in circles[0,:]:
        if abs(distPoint[0])>abs(centerImg[0]-c[0]) and abs(distPoint[1])>abs(centerImg[1]-c[1]):
            inner_circle[0] = c[0]
            distPoint[0] = abs(centerImg[0]-c[0])
            inner_circle[1] = c[1]
            distPoint[1] = abs(centerImg[1]-c[1])
            inner_circle[2] = c[2]
    centerx = (inner_circle[0]+centerImg[0])/2.1
    centery = (inner_circle[1]+centerImg[1])/2.1
    inner_circle = (centerx,centery,inner_circle[2])
    inner_circle = np.uint64(inner_circle)
    x1,y1,x2,y2 = drawRec(img.shape,centerx,centery,inner_circle[2], 1.6)
    img_crop = img[(x1):(x2), (y1):(y2)]
    img_hsv = cv2.cvtColor(img_crop, cv2.COLOR_BGR2HSV)
    hsv_value = img_hsv[:,:,2]
    edges = canny(hsv_value, sigma=3, low_threshold= 6, high_threshold=40)
    hough_radii = np.arange(14,45,1)
    hough_res = hough_circle(edges,hough_radii)
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=1)
    xs1,ys1,xs2,ys2 = drawRec(img_crop.shape, cy[0],cx[0],radii[0])
    img_crop2 = img_crop[(xs1):(xs2), (ys1):(ys2)]
    img_crop2 = cv2.cvtColor(img_crop2 ,cv2.COLOR_BGR2GRAY)
    return img_crop2

def drawRec(imgShape,x,y,r,divide = 1):
    top_left_x = int(max(0, x-r))
    top_left_y = int(max(0, y-r))
    bottom_right_x = int(min(imgShape[1],x + r))
    bottom_left_y = int(min(imgShape[0],y + r))
    if divide > 1:
        Ax = bottom_right_x - top_left_x
        Ay = bottom_left_y - top_left_y
        Ax2 = Ax/divide
        Ay2 = Ay/divide
        top_left_x = np.int32(top_left_x + ((Ax - Ax2)/2)) 
        top_left_y = np.int32(top_left_y + ((Ay - Ay2)/2)) 
        bottom_right_x = np.int32(top_left_x + Ax2) 
        bottom_left_y = np.int32(top_left_y + Ay2) 
    return top_left_x,top_left_y,bottom_right_x,bottom_left_y

def filterCircle(circles, img_shape):
    if len(circles) == 1:
        return circles[0]
    return circles[0]