import requests
import urllib.request
import threading
from bs4 import BeautifulSoup

#全局变量：页面的列表
PAGE_URL = ['http://www.doutula.com/photo/list/?page={}'.format(str(i)) for i in range(1,100)]
#全局变量：表情的列表
FACE_URL = [ ]
#全局变量：表情包的名字
T = [] 
#全局锁
gLock = threading.Lock()
#单线程用
#urls = ['http://www.doutula.com/photo/list/?page={}'.format(str(i)) for i in range(1,4)]

headers = {
   "User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11"    
 }
# =============================================================================
      #  非多线程代码获取网页链接与图片链接
# def get_pic(URL):
#     res = requests.get(URL,headers=headers)
#     all = BeautifulSoup(res.content,'lxml')
#     
#     img_url = all.find_all('img',attrs={'class':'img-responsive lazy image_dta'})
#     
#     #print(img_url)
#     
#     for img_i in img_url:
#         u = img_i['data-original']
#         t = img_i['alt']
#         if u.rfind('gif',0,len(u)) != -1:
#             ls = 'gif'
#         elif u.rfind('jpg',0,len(u)) != -1:
#             ls = 'jpg'
#         urllib.request.urlretrieve(u,'D:/anaconda/py项目/pic/%s.{}'.format(ls) % t )   
#         #x = x+1
#         #print(t)
#    
# 
# 
# =============================================================================
#  开启多线程    

def poducer():
    while True:
        gLock.acquire()
        if len(PAGE_URL) == 0:
            gLock.release()
            break
        else:
            URL = PAGE_URL.pop()
            #print(PAGE_URL)
            gLock.release()
            
            res = requests.get(URL,headers=headers)
            #print(res.content)
            all = BeautifulSoup(res.text,'lxml')
    
            img_url = all.find_all('img',attrs={'class':'img-responsive lazy image_dta'})
            
            gLock.acquire()
            for img_i in img_url:
                u = img_i['data-original']
                t = img_i['alt']
                #print(u)
                FACE_URL.append(u)
                T.append(t)
                #print(len(FACE_URL))
            gLock.release()



def customer():
    while True:
        #print(FACE_URL)
        gLock.acquire()
        if len(FACE_URL) ==0:
            gLock.release()
            continue
        else:
            img_j= FACE_URL.pop()
            title = T.pop()
            #print(img_j)
            gLock.release()
            
            #bug
#            u_d = img_j['data-original']
#           t_d = img_j['alt']
            
            if img_j.rfind('gif',0,len(img_j)) != -1:
                ls = 'gif'
            elif img_j.rfind('jpg',0,len(img_j)) != -1:
                ls = 'jpg'
            urllib.request.urlretrieve(img_j,'D:/anaconda/py项目/pic/{}.{}'.format(title,ls))  
        




#创建3个多线程作为生产者，去爬取url
def main():
    for x in range(3):
        muti_get_pic = threading.Thread(target=poducer)
        muti_get_pic.start()
        
        
#创建5个多线程作为生产者，去下载图片
    for x in range(5):
        muti_get_pic_2 = threading.Thread(target=customer)
        muti_get_pic_2.start()
        
        
        
    muti_get_pic.join()
    muti_get_pic_2.join()
if __name__ == "__main__":
    main()








