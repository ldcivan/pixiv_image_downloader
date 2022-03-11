# -*- coding:utf-8 -*-
import requests,os,json
import traceback
HEADERS={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
#访问头

print(
    '''
    ----------------------------------------

        Pixiv_Image_Downloader    V 1.0

                    originally build by:冷溪凌寒
                    develop by:Yujio_Nako
                    
    ----------------------------------------
    '''
)

source_list=[]#原图网站列表
img_list=[]#原图地址列表
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
    print("A total of %s submissions were found, now loading, please wait a moment..."%len(l))

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
            if (status == 404):
                temp = temp.replace('.jpg', '.png')
            #改为真实地址
            img.append(temp)
            #添加到图片ID列表
            print("Loading the %d image..."%num)
            num=num+1
    if len(img) == 0: #如果常规方法没找到链接则切换方法
        print("Can't find image, probably because target is a R-18 or private artwork")
        print("Use method 2...")
        urlb = source + "/artworks/" + source_list[i]
        response = requests.get(urlb, headers=HEADERS)
        first_target = re.search('"original":"(.+?)"},"tags"', response.text)   #直接到源码中找original
        temp = first_target.group(1)
        nPos = temp.index("_p0")
        if (nPos >= 0):
            temp_f = temp.split('_p0')[0] + "_p"
            temp_b = temp.split('_p0')[1]
            j = 0
            ifloop = 1
            while (ifloop == 1):
                temp = temp_f + str(j) + temp_b
                status = requests.get(temp, timeout=5).status_code
                if (status == 404):
                    ifloop = 0 #判断是否爬取了所有链接，404后则不再继续向后爬取
                else:
                    img.append(temp)
                    # 添加到图片ID列表
                    print("Loading the %d image..." %num)
                    num = num + 1
                    j = j + 1
        else:
            img.append(temp)
    print("A total of %s images were found"%len(img))
    #time.sleep(1)

def mkdir(s):#创建文件夹
    isExists=os.path.exists(s)#判断是否创建了文件夹
    if not isExists:
        os.makedirs(s)#创建文件夹
        print("Creating file '%s', the images will place in the file '%s'."%(s,s))
    else:
        print("File '%s' has been created, the images will place in the file '%s'."%(s,s))

def download(s,img):
    num = 1
    print('------------------------------------------------------------------------------')
    print('No.\t\t\timg_url')
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
        print("Image No.%s has been downloaded."%num)
        print("%s.\t\t\t%s"%(num,img[i]))
        num = num+1
    print('------------------------------------------------------------------------------')
    print("Complete!")

while(loop==''):
    method = int(input("Download with the ID of?(1.Illustrator's 2.Image's):"))
    file_name = input("Please enter the file name to save to (If left blank, the default is Illustrator Name/Image ID):")
    #
    print('------------------------------------------------------------------------------')
    print("Choosing host，please wait for about 5 seconds...")
    url = "https://www.pixiv.net"
    try:
        status = requests.get(url, timeout=5, verify=False).status_code
        if status == 200:
            source = "https://www.pixiv.net"
            print("Using host:pixiv.net")
    except:
        source = "https://pixiv.pro-ivan.cn"
        #备选Host，不适用
        #source = "https://pixiv.re"
        print("Using host:pixiv.pro-ivan.cn")
    #选择host
    if (method == 1):
        print('------------------------------------------------------------------------------')
        search = input("Please enter the Illustrator_ID you want to search:")
        if not (file_name):
            file_name = search
            print("The folder has named with Illustrator_ID")
        search_user(search, source_list)
        search_source(img_list)
        mkdir(file_name)
        download(file_name, img_list)
    if (method == 2):
        print('------------------------------------------------------------------------------')
        illusion = input("Please enter the Image_ID you want to search:")
        if not (file_name):
            file_name = illusion
            print("The folder has named with Image_ID")
        source_list = [illusion]
        search_source(img_list)
        mkdir(file_name)
        download(file_name, img_list)
    #输入作者/作品ID
    traceback.print_exc()
    if img_list == []:
        print("Can't find image anyway, probably because target is a private artwork")
    print("If program shut down, contact us with error log. Or Ignore the log.")
    print('------------------------------------------------------------------------------')
    loop == input("Press Enter to download other images...")