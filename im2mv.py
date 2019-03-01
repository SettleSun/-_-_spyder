# -*- coding:utf-8 -*-

import cv2
import glob
from PIL import Image
import numpy as np
def im2vedio( mv_name,fps): 
    #可以用(*'DVIX')或(*'X264'),如果都不行先装ffmepg: sudo apt-get install ffmepg
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    #saveVideo.avi是要生成的视频名称，（384,288）是图片尺寸
    videoWriter = cv2.VideoWriter(mv_name,fourcc,fps,(384,288))#括号可能是中文的，改一下，384,288需要改成你的图片尺寸，不然会报错
    #imge存放图片
    imgs=glob.glob('/root/a_new/yolov3/My_data/im_data/Chinese_fighter_aircraft/*.jpg')
    for imgname in imgs:
        img = cv2.imread(imgname)
        #CV_INTER_NN - 最近邻插值,  
        #CV_INTER_LINEAR - 双线性插值 (缺省使用)  
        #CV_INTER_AREA - 使用象素关系重采样。当图像缩小时候，该方法可以避免波纹出现。当图像放大时，类似于 CV_INTER_NN 方法..  
        #CV_INTER_CUBIC - 立方插值.  
        frame = cv2.resize(img,(384,288),interpolation=cv2.CV_INTER_AREA)  #想调整的大小
        videoWriter.write(frame)
    videoWriter.release()


if __name__ == '__main__':
    sp_new = 'znew.avi'
    im2vedio(sp_new, 2)  # 图片转视频
