# -*- coding:utf-8 -*-
## tab=space4
import os
## "潜T：0=>20  ||person：1=>14 ||ship：2=>3 ||直升J：3=>21  ||gun：4=>22"\
## "tank：5=>23 ||战斗J：6=>24  ||航M：7=>25  ||J20：8=>26    ||J15：9=>27"\
## "J10：10=>28 ||预J：11=>29   ||客机：12=>0 ||加油J：13=>30 ||B2：14=>31"\
## "F-A：15=>32 ||F16：16=>33   ||F22：17=>34 ||F35：18=>35   ||s35：19=>36"\
class_num = [20,14,3,21,22,23,24,25,26,27,28,29,0,30,31,32,33,34,35,36,-1]
write_file = open("labels.txt",'a+',encoding = 'utf-8')
def main(labes_txt_path):
    ## 
    txt_names = os.listdir(labes_txt_path)
    for txt_name in txt_names:
        ## 文件夹路径+txt文件名
        txt_path_plus_name = labes_txt_path+txt_name
        print(txt_path_plus_name)
        with open(txt_path_plus_name) as input_txt:
            write_labels = ""
            while True:
                txt_data = next(input_txt,"gg").strip()
                if txt_data == "":
                    continue## 空行继续
                if txt_data == "gg":
                    break## 结束
                ## 数据处理
                data_list = txt_data.split(" ")                   
                ## box x_min y_min x_max y_max + id clsaa+ old info
                if class_num[int(data_list[4])]==-1:continue
                write_labels = write_labels+" "+" ".join(data_list[0:4])+" "+str(class_num[int(data_list[4])])
            ## txt 文本为空 跳过
            if write_labels == "":
                print(txt_name)
                continue 
            ## 写入数据
            write_labels = "./raccoon_dataset/images/"+txt_name.split(".txt")[0]+".jpg"+write_labels+"\r\n"
            write_file.write(write_labels)
                
        #break
    write_file.close()
                    
if __name__ == "__main__":
    main("./data2CETC_labels/")





