import cv2
import numpy as np
from enum import Enum
import itertools
from shapely.geometry import Polygon
from .File import *
from .Math import *
from scipy.spatial import ConvexHull
class cv_colors(Enum):
    RED = (0,0,255)
    GREEN = (0,255,0)
    BLUE = (255,0,0)
    PURPLE = (247,44,200)
    ORANGE = (44,162,247)
    MINT = (239,255,66)
    YELLOW = (2,255,250)

def constraint_to_color(constraint_idx):
    return {
        0 : cv_colors.PURPLE.value, #left
        1 : cv_colors.ORANGE.value, #top
        2 : cv_colors.MINT.value, #right
        3 : cv_colors.YELLOW.value #bottom
    }[constraint_idx]


# from the 2 corners, return the 4 corners of a box in CCW order
# coulda just used cv2.rectangle haha
def create_2d_box(box_2d):
    corner1_2d = box_2d[0]
    corner2_2d = box_2d[1]

    pt1 = corner1_2d
    pt2 = (corner1_2d[0], corner2_2d[1])
    pt3 = corner2_2d
    pt4 = (corner2_2d[0], corner1_2d[1])

    return pt1, pt2, pt3, pt4


# takes in a 3d point and projects it into 2d
def project_3d_pt(pt, cam_to_img, calib_file=None):
    if calib_file is not None:
        cam_to_img = get_calibration_cam_to_image(calib_file)
        R0_rect = get_R0(calib_file)
        Tr_velo_to_cam = get_tr_to_velo(calib_file)

    point = np.array(pt)
    point = np.append(point, 1)

    point = np.dot(cam_to_img, point)
    # point = np.dot(np.dot(np.dot(cam_to_img, R0_rect), Tr_velo_to_cam), point)

    point = point[:2]/point[2]
    point = point.astype(np.int16)

    return point

def make_polygon(points:list):
    hull = ConvexHull(points)  # put points in order to avoid self-intersection
    polygon = Polygon(hull.points)
    return polygon

# take in 3d points and plot them on image as red circles
def plot_3d_pts(img, pts, center, calib_file=None, cam_to_img=None, relative=False, constraint_idx=None):
    if calib_file is not None:
        cam_to_img = get_calibration_cam_to_image(calib_file)

    for pt in pts:
        if relative:
            pt = [i + center[j] for j,i in enumerate(pt)] # more pythonic

        point = project_3d_pt(pt, cam_to_img)

        color = cv_colors.RED.value

        if constraint_idx is not None:
            color = constraint_to_color(constraint_idx)

        cv2.circle(img, (point[0], point[1]), 3, color, thickness=-1)



def plot_3d_box(img, cam_to_img, ry, dimension, center,poly):

    # plot_3d_pts(img, [center], center, calib_file=calib_file, cam_to_img=cam_to_img)

    R = rotation_matrix(ry)

    corners = create_corners(dimension, location=center, R=R)

    # to see the corners on image as red circles
    plot_3d_pts(img, corners, center,cam_to_img=cam_to_img, relative=False)

    box_3d = []
    # colour =cv_colors.RED.value if crossing else cv_colors.GREEN.value
    colour =cv_colors.ORANGE.value
    for corner in corners:
        point = project_3d_pt(corner, cam_to_img)
        box_3d.append(point)

    bottom_points=[(box_3d[0][0], box_3d[0][1]), (box_3d[4][0],box_3d[4][1]),
                   (box_3d[1][0], box_3d[1][1]), (box_3d[5][0],box_3d[5][1])]
    bottom_points=[(i[1],i[0]) for i in bottom_points]
    poly_1=make_polygon(bottom_points)
    print('poly1',poly_1.exterior.xy)
    poly_2=poly
    # poly_2=Polygon([[929,87],[1353,145],[1338,145],[913,123]])
    colour = cv_colors.RED.value if poly_1.intersects(poly_2) else cv_colors.GREEN.value
    print('intersection',poly_1.intersects(poly_2))
    # print('intersection111',poly_1.intersection(poly_2))
    #TODO put into loop
    cv2.line(img, (box_3d[0][0], box_3d[0][1]), (box_3d[2][0],box_3d[2][1]), colour, 1)
    cv2.line(img, (box_3d[4][0], box_3d[4][1]), (box_3d[6][0],box_3d[6][1]), colour, 1)
    cv2.line(img, (box_3d[0][0], box_3d[0][1]), (box_3d[4][0],box_3d[4][1]), colour, 1) # low line
    cv2.line(img, (box_3d[2][0], box_3d[2][1]), (box_3d[6][0],box_3d[6][1]), colour, 1)

    cv2.line(img, (box_3d[1][0], box_3d[1][1]), (box_3d[3][0],box_3d[3][1]), colour, 1)
    cv2.line(img, (box_3d[1][0], box_3d[1][1]), (box_3d[5][0],box_3d[5][1]), colour, 1) # low line
    cv2.line(img, (box_3d[7][0], box_3d[7][1]), (box_3d[3][0],box_3d[3][1]), colour, 1)
    cv2.line(img, (box_3d[7][0], box_3d[7][1]), (box_3d[5][0],box_3d[5][1]), colour, 1)

    for i in range(0,7,2):
    # for i in [2,6]: # [0,4] - 2 нижние линии
        cv2.line(img, (box_3d[i][0], box_3d[i][1]), (box_3d[i+1][0],box_3d[i+1][1]), colour, 1)

    front_mark = [(box_3d[i][0], box_3d[i][1]) for i in range(4)]

    # cv2.line(img, front_mark[0], front_mark[3], cv_colors.BLUE.value, 1)
    # cv2.line(img, front_mark[1], front_mark[2], cv_colors.BLUE.value, 1)

def plot_2d_box(img, box_2d):
    # create a square from the corners
    pt1, pt2, pt3, pt4 = create_2d_box(box_2d)

    # plot the 2d box
    # cv2.line(img, pt1, pt2, cv_colors.BLUE.value, 2)
    # cv2.line(img, pt2, pt3, cv_colors.BLUE.value, 2)
    # cv2.line(img, pt3, pt4, cv_colors.BLUE.value, 2)
    # cv2.line(img, pt4, pt1, cv_colors.BLUE.value, 2)


def poly_by_border(border_file):
    # img = cv2.imread(img_file)
    border = cv2.imread(border_file)
    # print(np.unique(border))
    # cond=np.where(np.any(border !=[0,0,0], axis=-1))
    # cond = np.where(np.any(border > 200, axis=-1))
    # print(cond)
    # img[20:200,100:500,:]=(0,0,255)
    # img[cond] = (0, 0, 255)
    border[np.where(np.any(border > 0, axis=-1))] = (0, 0, 255)
    # print(np.where(np.any(border[0] > 254, axis=-1)))
    # print(border!=0)
    # img=img+border
    # cv2.imshow('fff', img)
    cv2.waitKey(0)

    img_gray = cv2.cvtColor(border, cv2.COLOR_BGR2GRAY)

    # apply binary thresholding
    ret, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY)
    #cv2.imshow('Binary image', thresh)
    cv2.waitKey(0)
    cv2.imwrite('image_thres1.jpg', thresh)
    cv2.destroyAllWindows()
    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
    # print('len(contours) ',len(contours))
    # print(contours[len(contours)-1][0])
    # draw contours on the original image
    image_copy = border.copy()
    contour = contours[len(contours) - 1]
    contour = np.array([i[0] for i in contour])
    contour=[(i[1],i[0]) for i in contour]
    # print(contour)
    from scipy.spatial import ConvexHull
    hull = ConvexHull(contour)
    poly = Polygon(hull.points)
    # print('poly', poly.exterior.xy)

    # cv2.drawContours(image=image_copy, contours=contour, contourIdx=-1, color=(0, 255, 0), thickness=2,
    #                  lineType=cv2.LINE_AA)
    #
    # # see the results
    # cv2.imshow('None approximation', image_copy)
    # cv2.waitKey(0)
    # cv2.imwrite('contours_none_image1.jpg', image_copy)
    # cv2.destroyAllWindows()
    return  poly