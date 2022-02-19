# -*- coding:utf-8 -*-
import requests,os,json
import traceback
HEADERS={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
#访问头

print(
    '''
    ----------------------------------------

            获取Pixiv图片    V 1.0

                    originally build by:冷溪凌寒
                    develop by:Yujio_Nako
                    
    ----------------------------------------
    '''
)

source_list = []#原图网站列表
img_list = []#原图地址列表
loop = ''

def search_user(s,l):
    url= source+"/ajax/user/"+s+"/profile/all?lang=zh"
    HEADERS['Referer'] = url
    #更改Referer，通过反爬虫机制
    page = requests.get(url, headers=HEADERS).text
    #获取作者主页json
    json_user=json.loads(page).get('body').get('illusts')
    for i in json_user.keys():
        l.append(i)
        #添加到投稿ID列表
    print("一共找到了%s次投稿，加载中，请稍等..."%len(l))

def search_source(img):
    num=1
    for i in range(0,len(source_list)):     #遍历所有投稿
        url = source+"/ajax/illust/"+source_list[i]+"/pages?lang=zh"
        #进入投稿页面
        HEADERS['Referer'] = url
        #更改Referer，通过反爬虫机制
        page = requests.get(url, headers=HEADERS).text
        #获取投稿页json
        json_illust=json.loads(page).get('body')
        #获取json内的body列表
        for j in json_illust:
            temp=j['urls']
            #获取body列表内的urls字典
            temp=temp['regular']
            #获取键为"regular"的值
            temp = temp.replace('img-master', 'img-original')
            temp = temp.replace('_master1200', '')
            status = requests.get(temp, timeout=5).status_code
            if(status==404):
                temp = temp.replace('.jpg', '.png')
            #改为真实地址
            img.append(temp)
            #添加到图片ID列表
            print("加载第%d张图片..."%num)
            num=num+1
    print("一共获取到了%s张图片。"%len(img))
    #time.sleep(1)

def mkdir(s):#创建文件夹
    isExists=os.path.exists(s)#判断是否创建了文件夹
    if not isExists:
        os.makedirs(s)#创建文件夹
        print("创建文件夹'%s'，将图片放入'%s'文件夹内。"%(s,s))
    else:
        print("已经有'%s'文件夹，将图片放入'%s'文件夹内。"%(s,s))

def download(s,img):
    num = 1
    print('------------------------------------------------------------------------------')
    print('序号\t\t\t图片链接')
    for i in range(0,len(img)):
        a = requests.get(url=img[i],headers=HEADERS)
        name = img[i].split('/')[-1]
        name = str(name).replace('[\'','')
        name = str(name).replace('\']', '')
        name = str(name).replace('\',\'', '')
        if (method == 1):
            f = open(search+"/%s.png"%num, 'wb')#以二进制格式写入文件夹中
        if (method == 2):
            f = open(illusion + "/%s.png" % name, 'wb')
        f.write(a.content)
        f.close()
        print("第%s张图片下载完毕；"%num)
        print("%s.\t\t\t%s"%(num,img[i]))
        num = num+1
    print('------------------------------------------------------------------------------')
    print("下载结束！")

while(loop==''):
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
    #选择host
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
    #输入作者/作品ID
    traceback.print_exc()
    print("如程序出错，请附上日志与我们联系。否则，请无视输出的日志。")
    print('------------------------------------------------------------------------------')
    loop == input("回车以继续下载...")
