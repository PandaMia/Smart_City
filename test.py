import numpy as np
import cv2
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
img_file="C:/Users\y.sobolev\Desktop/trash/photo_2021-12-04_01-04-53.jpg"
border_file="C:/Users\y.sobolev\Desktop/trash\photo_2\photo_2.jpg"

def poly_by_border(img_file, border_file):
    img=cv2.imread(img_file)
    border=cv2.imread(border_file)
    print(np.unique(border))
    # cond=np.where(np.any(border !=[0,0,0], axis=-1))
    cond=np.where(np.any(border>200, axis=-1))
    print(cond)
    # img[20:200,100:500,:]=(0,0,255)
    img[cond]=(0,0,255)
    border[np.where(np.any(border>0, axis=-1))]=(0,0,255)
    print(np.where(np.any(border[0] >254, axis=-1)))
    # print(border!=0)
    # img=img+border
    cv2.imshow('fff',img)
    cv2.waitKey(0)

    img_gray = cv2.cvtColor(border, cv2.COLOR_BGR2GRAY)

        # apply binary thresholding
    ret, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY)
    cv2.imshow('Binary image', thresh)
    cv2.waitKey(0)
    cv2.imwrite('image_thres1.jpg', thresh)
    cv2.destroyAllWindows()
    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
    # print('len(contours) ',len(contours))
    # print(contours[len(contours)-1][0])
    # draw contours on the original image
    image_copy = border.copy()
    contour=contours[len(contours)-1]
    contour=np.array([i[0] for i in contour])
    # print(contour)
    from scipy.spatial import ConvexHull
    hull=ConvexHull(contour)
    poly=Polygon(hull.points)
    # print('poly', poly.exterior.xy)

    cv2.drawContours(image=image_copy, contours=contour, contourIdx=-1, color=(0, 255, 0), thickness=2,
                     lineType=cv2.LINE_AA)

    # see the results
    cv2.imshow('None approximation', image_copy)
    cv2.waitKey(0)
    cv2.imwrite('contours_none_image1.jpg', image_copy)
    cv2.destroyAllWindows()
    return img,poly

img_file="C:/Users\y.sobolev\Desktop/trash/photo_2021-12-04_01-04-53.jpg"
border_file="C:/Users\y.sobolev\Desktop/trash\photo_2\photo_2.jpg"
poly_by_border(img_file, border_file)