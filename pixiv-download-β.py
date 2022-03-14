# -*- coding:utf-8 -*-
import requests, re, os, json
import traceback
import cv2
import numpy as np

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
# 访问头

print(
    '''
    ----------------------------------------

            获取Pixiv图片    V 1.0

                    originally build by:冷溪凌寒
                    develop by:Yujio_Nako

    ----------------------------------------
    '''
)

source_list = []  # 原图网站列表
img_list = []  # 原图地址列表
loop = ''


def search_user(s, l):
    url = source + "/ajax/user/" + s + "/profile/all?lang=zh"
    HEADERS['Referer'] = url
    # 更改Referer，通过反爬虫机制
    page = requests.get(url, headers=HEADERS).text
    # 获取作者主页json
    json_user = json.loads(page).get('body').get('illusts')
    for i in json_user.keys():
        l.append(i)
        # 添加到投稿ID列表
    print("一共找到了%s次投稿，加载中，请稍等..." % len(l))


def search_source(img):
    num = 1
    for i in range(0, len(source_list)):  # 遍历所有投稿
        urlb = source + "/artworks/" + source_list[i]
        response = requests.get(urlb, headers=HEADERS)
        first_target = re.search('"original":"(.+?)"},"tags"', response.text)  # 直接到源码中找original
        temp = first_target.group(1)
        try:
            nPos = temp.index("_p0")
        except:
            nPos = -1
        if (nPos >= 0):
            temp_f = temp.split('_p0')[0] + "_p"
            temp_b = temp.split('_p0')[1]
            j = 0
            ifloop = 1
            while (ifloop == 1):
                try:
                    temp = temp_f + str(j) + temp_b
                    status = requests.get(temp, timeout=5).status_code
                    if (status == 404):
                        ifloop = 0  # 判断是否爬取了所有链接，404后则不再继续向后爬取
                    else:
                        img.append(temp)
                        # 添加到图片ID列表
                        print("加载第%s张图片..." % num)
                        num = num + 1
                        j = j + 1
                except:
                    j = j
        else:
            img.append(temp)
    print("一共获取到了%s张图片。" % len(img))
    # time.sleep(1)


def mkdir(s):  # 创建文件夹
    isExists = os.path.exists(s)  # 判断是否创建了文件夹
    if not isExists:
        os.makedirs(s)  # 创建文件夹
        print("创建文件夹'%s'，将图片放入'%s'文件夹内。" % (s, s))
    else:
        print("已经有'%s'文件夹，将图片放入'%s'文件夹内。" % (s, s))


def download(s, img):
    num = 1
    print('------------------------------------------------------------------------------')
    print('序号\t\t\t图片链接')
    for i in range(0, len(img)):
        try:
            mPos = img[i].index("_ugoira0")
        except:
            mPos = -1
        if(mPos >= 0):
            print("检测到GIF，将下载到temp，请稍后自行合并为视频")
            download_gif(s,img[i])
        else:
            a = requests.get(url=img[i], headers=HEADERS)
            name = img[i].split('/')[-1]
            name = str(name).replace('[\'', '')
            name = str(name).replace('\']', '')
            name = str(name).replace('\',\'', '')
            if (method == 1):
                f = open(search + "/%s.png" % num, 'wb')  # 以二进制格式写入文件夹中
            if (method == 2):
                f = open(illusion + "/%s.png" % name, 'wb')
            f.write(a.content)
            f.close()
            print("第%s张图片下载完毕；" % num)
            print("%s.\t\t\t%s" % (num, img[i]))
            num = num + 1
    print('------------------------------------------------------------------------------')
    print("下载结束！")

def download_gif(s, img):
    nPos = img.index("_ugoira0")
    img2 = []
    if (nPos >= 0):
        temp_f = img.split('_ugoira0')[0] + "_ugoira"
        temp_b = img.split('_ugoira0')[1]
        j = 0
        nummber = 1
        ifloop = 1
        while (ifloop == 1):
            try:
                temp = temp_f + str(j) + temp_b
                status = requests.get(temp, timeout=5).status_code
                if (status == 404):
                    ifloop = 0  # 判断是否爬取了所有链接，404后则不再继续向后爬取
                else:
                    img2.append(temp)
                    # 添加到图片ID列表
                    print("加载动图的第%s张图片..." % nummber)
                    nummber = nummber + 1
                    j = j + 1
            except:
                j = j
    else:
        img2.append(img)
    number = 1
    print('------------------------------------------------------------------------------')
    print('正在下载动图')
    print('序号\t\t\t图片链接')
    if (method == 1):
        mkdir(search + "/" + temp_f +"_temp/")
        file2change = search + "/" + temp_f +"_temp/"
        upfile2change = search + "/"
    if (method == 2):
        mkdir(illusion + "/temp")
        file2change = illusion + "/temp/"
        upfile2change = illusion + "/"
    for i in range(0, len(img2)):
        try:
            a = requests.get(url=img2[i], headers=HEADERS)
            name = img2[i].split('/')[-1]
            name = str(name).replace('[\'', '')
            name = str(name).replace('\']', '')
            name = str(name).replace('\',\'', '')
            if (method == 1):
                f = open(search + "/%s_temp/%s.png" % temp_f % name, 'wb')  # 以二进制格式写入文件夹中
            if (method == 2):
                f = open(illusion + "/temp/%s.png" % name, 'wb')
            f.write(a.content)
            f.close()
            print("%s.\t\t\t%s" % (number, img2[i]))
            number = number + 1
        except:
            number = number
    name2change = img2[0].split('/')[-1]
    name2change = str(name2change).replace('[\'', '')
    name2change = str(name2change).replace('\']', '')
    name2change = str(name2change).replace('\',\'', '')
    pic2video(file2change, name2change,upfile2change)
    print('------------------------------------------------------------------------------')
    print("%s下载结束！" % name)

def pic2video(file,name,upfile):
    fn= file + name + ".png"
    sz1 = 0
    sz2 = 0
    if __name__ == '__main__':
        print ('load %s as ...' % fn)
        img = cv2.imread(fn)
        sp = img.shape
        print (sp)
        sz1 = sp[0]#height(rows) of image
        sz2 = sp[1]#width(colums) of image
        print ('width: %d \nheight: %d ' %(sz1,sz2))
    fps = 12
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(upfile+name + '.avi', fourcc, fps, (sz2,sz1), True)
    name_f = name.split('_ugoira0')[0] + "_ugoira"
    name_b = name.split('_ugoira0')[1]
    print("开始合并")
    print(file + name_f +"0"+ name_b + '.png')
    for i in range(0,401):
        p = i
        # print(str(p)+'.png'+'233333')
        if os.path.exists(file + name_f +str(p)+ name_b + '.png'):
            img = cv2.imread(filename=file + name_f + str(p) + name_b + '.png')
            cv2.imshow('img', img)
            cv2.waitKey(100)
            video_writer.write(img)
            print(str(p) + '.png' + 'Yes!')
    video_writer.release()
    print("合并完成")


while (loop == ''):
    method = int(input("请输入想要使用的方法(1.按作者id 2.按作品id):"))
    file_name = input("请输入保存到的文件夹名(留空则默认为作者名/作品id):")
    #
    print('------------------------------------------------------------------------------')
    print("正在选择host，约需要5秒...")
    url = "https://www.pixiv.net"
    try:
        status = requests.get(url, timeout=5, verify=False).status_code
        if status == 200:
            source = "https://www.pixiv.net"
            print("已使用host:pixiv.net")
    except:
        source = "https://pixiv.pro-ivan.cn"
        # 备选Host，不适用
        # source = "https://pixiv.re"
        print("已使用host:pixiv.pro-ivan.cn")
    # 选择host
    if (method == 1):
        print('------------------------------------------------------------------------------')
        search = input("请输入想要搜索的作者id:")
        if not (file_name):
            file_name = search
            print("文件夹命名为作者id")
        search_user(search, source_list)
        search_source(img_list)
        mkdir(file_name)
        download(file_name, img_list)
    if (method == 2):
        print('------------------------------------------------------------------------------')
        illusion = input("请输入作品id:")
        if not (file_name):
            file_name = illusion
            print("文件夹命名为作品id")
        source_list = [illusion]
        search_source(img_list)
        mkdir(file_name)
        download(file_name, img_list)
    # 输入作者/作品ID
    traceback.print_exc()
    if img_list == []:
        print("依旧未找到图片，可能是因为目标是私人稿件")
    print("如程序出错，请附上日志与我们联系。否则，请无视输出的日志。")
    print('------------------------------------------------------------------------------')
    loop == input("回车以继续下载...")