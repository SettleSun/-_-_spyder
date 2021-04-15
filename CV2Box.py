import cv2 as cv
import numpy as np

events = [print(i) for i in dir(cv) if 'EVENT' in i]
'''=============================================================
                        鼠标画框
============================================================='''
drawing = False # 如果按下鼠标，则为真
ix,iy = -1,-1

# 鼠标回调函数
def draw_circle2(event,x,y,flags,param):
    global ix,iy,drawing
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    # elif event == cv.EVENT_MOUSEMOVE:
    #     if drawing == True:
    #         cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        cv.rectangle(img,(ix,iy),(x,y),(0,255,0),2)# -1,0,2
# 创建一个黑色的图像，一个窗口，并绑定到窗口的功能
img = np.zeros((512,512,3), np.uint8)
cv.namedWindow('image')
cv.setMouseCallback('image',draw_circle2)
while(1):
    cv.imshow('image',img)
    if cv.waitKey(20) & 0xFF == 27:
        break
    if cv.waitKey(20) == ord('q'):
        break
cv.destroyAllWindows()
'''=============================================================
        框选颜色
============================================================='''
def nothing(x):
    pass
# 创建一个黑色的图像，一个窗口
img = np.zeros((300,512,3), np.uint8)
cv.namedWindow('image')
# 创建颜色变化的轨迹栏
cv.createTrackbar('R','image',0,255,nothing)
cv.createTrackbar('G','image',0,255,nothing)

cv.createTrackbar('B','image',0,255,nothing)
# 为 ON/OFF 功能创建开关
switch = '0 : OFF \n1 : ON'
cv.createTrackbar(switch, 'image',0,1,nothing)
while(1):
    cv.imshow('image',img)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
    # 得到四条轨迹的当前位置
    r = cv.getTrackbarPos('R','image')
    g = cv.getTrackbarPos('G','image')
    b = cv.getTrackbarPos('B','image')
    s = cv.getTrackbarPos(switch,'image')
    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]
cv.destroyAllWindows()
#===========================================================================


