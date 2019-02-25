# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 09:32:02 2016

@author: http://blog.csdn.net/lql0716
"""
import cv2
import numpy as np
import os

current_pos = None
tl = None
br = None

#鼠标事件
def get_rect(im_path, title='get_rect'):   #   (a,b) = get_rect(im, title='get_rect')
    im = cv2.imread(im_path)
    mouse_params = {'tl': None, 'br': None, 'current_pos': None,
        'released_once': False}

    cv2.namedWindow(title)
    cv2.moveWindow(title, 100, 100)

    def onMouse(event, x, y, flags, param):

        param['current_pos'] = (x, y)

        if param['tl'] is not None and not (flags & cv2.EVENT_FLAG_LBUTTON):
            param['released_once'] = True

        if flags & cv2.EVENT_FLAG_LBUTTON:
            if param['tl'] is None:
                param['tl'] = param['current_pos']
            elif param['released_once']:
                param['br'] = param['current_pos']

    cv2.setMouseCallback(title, onMouse, mouse_params)
    cv2.imshow(title, im)

    while mouse_params['br'] is None:
        im_draw = np.copy(im)

        if mouse_params['tl'] is not None:
            cv2.rectangle(im_draw, mouse_params['tl'],
                mouse_params['current_pos'], (255, 0, 0))

        cv2.imshow(title, im_draw)
        _ = cv2.waitKey(10)

    cv2.destroyWindow(title)

    tl = (min(mouse_params['tl'][0], mouse_params['br'][0]),
        min(mouse_params['tl'][1], mouse_params['br'][1]))
    br = (max(mouse_params['tl'][0], mouse_params['br'][0]),
        max(mouse_params['tl'][1], mouse_params['br'][1]))

    return (tl, br)  #tl=(y1,x1), br=(y2,x2)

def listdir(path):  # 读取文件夹 中的文件存储到list
    #path = 'im_data/'
    filenames = os.listdir(path)
    for filename in filenames:
        print(filename)
def renamefile():## 重命名图片
    path = 'im_data/'
    count = 1
    for file in os.listdir(path):
        os.rename(os.path.join(path,file),os.path.join(path,str(count)+".jpg"))
        count+=1         


def im_box(image_path):
    write_im_class_plus_id = open("class_plus_class/id.txt",'a+',encoding="utf-8")
    im_id = 333
    write_path_flag = 0
    while im_id != -1:
        (tl, br) = get_rect(image_path)
        ## 图框坐标
        x1_y1_x2_y2 = ','.join([str(tl[0]), str(tl[1]), str(br[0]), str(br[1])])
        im_id = int(input("输入框选ID或者-1，-1表示下一张图片:"))
        if im_id != -1:
            if write_path_flag == 0:
                write_path_flag = 1
                write_im_class_plus_id.write(image_path+',')        
            box_info = str(im_id)+','+x1_y1_x2_y2+","
            write_im_class_plus_id.write(box_info)
    write_im_class_plus_id.write('\r\n')
    write_im_class_plus_id.close()
            
  

def main():
    im_data_path = 'im_data/'
    im_names = os.listdir(im_data_path)
    for image_name in im_names:
        # 图像路径+图像名称
        image_path = im_data_path+image_name
        im_box(image_path)    
        
if __name__ == "__main__":
    main()













