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
    return (tl, br)  #tl=(x1,y1), br=(x2,y2)



def im_box(image_path):
    ## 标签保存路径+txt文件文件名
    write_im_box_id = open(image_path.split("tank_word")[0]+"tank_word_labels/"+image_path.split("tank_word/")[1].split('.jpg')[0]+".txt",'a+',encoding="utf-8")
    imginfo = cv2.imread(image_path).shape#(h,w,通道数)
    im_h = imginfo[0]
    im_w = imginfo[1]
    im_id = 333333
    while im_id != -1:
        (tl, br) = get_rect(image_path)
        ## 图框坐标
        x1_y1_x2_y2 = ' '.join([str(tl[0]), str(tl[1]), str(br[0]), str(br[1])])
        ##x1_y1_x2_y2 = ' '.join([str((tl[0]+br[0])/2.0/im_w), str((tl[1]+br[1])/2.0/im_h), str(abs(tl[0]-br[0])/im_w), str(abs(tl[1]-br[1])/im_h)])
        im_id = int(input("person=1、ship=2、直升机=3\r\nQT=0、gun=4、tank=5、air=6\r\n输入框选ID或者-1，-1表示下一张图片:"))
        if im_id != -1:   
            ## x_min,y_min,x_max,y_max,box_class_id                
            box_info = x1_y1_x2_y2+' '+str(im_id)+'\r\n'
            write_im_box_id.write(box_info)
    write_im_box_id.close()
            
  

def main():
    ## 图片路径
    im_data_path = './im_data/tank_word/'
    im_names = os.listdir(im_data_path)
    ## 中断重标
    skip_flage = 0    
    last_im = input("输入上次最后标注的图片名称编号：")
    last_im =im_data_path+'tank_word_'+last_im +'.jpg'
    im_num = 0
    for image_name in im_names:
        # 图像路径+图像名称
        image_path = im_data_path+image_name
        ## 打印当前标注的图片名称 应该写成首次自动读取？保存
        im_num += 1
        print(im_num,":=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:",image_name)
        if skip_flage==0 and image_path != last_im:
            continue
        skip_flage = 1
        im_box(image_path) 

'''
xxx/xxx.jpg 18.19 6.32 424.13 421.83 20 323.86 2.65 640.0 421.94 20 
xxx/xxx.jpg 55.38 132.63 519.84 380.4 16
image_path x_min y_min x_max y_max class_id  x_min y_min ... class_id 
'''                   
if __name__ == "__main__":
    main()
    
    













