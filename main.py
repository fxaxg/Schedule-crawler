"""
作者：陈同学
tips：代码写得烂，将就看，大佬可以自己改一下
日期：2023-08-30
描述：爬取所有课表，并将课表转换为图片
支持的学校：林业科技大学涉外学院
支持库：requests、base64、BeautifulSoup、gzip、io、PIL、imgkit、urllib，其中imgkit需要安装wkhtmltopdf。
"""



import os
import base64
from bs4 import BeautifulSoup
import requests
import gzip
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import imgkit
import urllib.parse

username = '在此输入你的学号'
password = '在此输入你的密码'
marjor = '专业，例如：Film_0202'



# 将学号和密码进行base64编码
encoded_username = base64.b64encode(username.encode("utf-8")).decode("utf-8")
encoded_password = base64.b64encode(password.encode("utf-8")).decode("utf-8")

# Step 1: 获取cookies
url = 'http://zswxyjw.yinghuaonline.com/znlykjdxswxy_jsxsd/'
response = requests.get(url)
cookies = response.cookies


# Step 2: 发送POST请求登录
login_url = 'http://zswxyjw.yinghuaonline.com/znlykjdxswxy_jsxsd/xk/LoginToXk'

# 组装请求参数
data = encoded_username + '%%%' + encoded_password
# data = r'encoded=MjAyMzAyMzEyMg%3D%3D%25%25%25U3loLjAxMTEwOQ%3D%3D'

# 进行URL编码
encoded_data = 'encoded=' + urllib.parse.quote(data)

print(encoded_data)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'zswxyjw.yinghuaonline.com',
    'Origin': 'http://zswxyjw.yinghuaonline.com',
    'Referer': 'http://zswxyjw.yinghuaonline.com/znlykjdxswxy_jsxsd/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'keep-alive': 'True'
}

response = requests.post(login_url, data=encoded_data,
                         headers=headers, cookies=cookies)
response_data = response.content

# 将返回的数据解码
response_data = response_data.decode(response.encoding)


# step 3: 获取课表

# 循环获取每一周的课表，目前看来，最多只有16周
for i in range(1, 17):
    url = "http://zswxyjw.yinghuaonline.com/znlykjdxswxy_jsxsd/xskb/xskb_list.do"

    data = "cj0701id=&zc=" + str(i) + "&demo=&xnxq01id=2023-2024-1&sfFD=1"

    response = requests.post(url, data=data, headers=headers, cookies=cookies)

    en_response = response.content.decode(response.encoding)

    # step 4: 解析课表
    # 创建BeautifulSoup对象，指定解析器为lxml
    soup = BeautifulSoup(en_response, 'lxml')

    table = soup.find('table', id='kbtable')

    # 如果找到了table元素
    if table:
        # 获取table元素内的所有内容
        contents = table.contents
        # 拼接table内容，并设置字体为微软雅黑
        table_data = '<table style="font-family:微软雅黑;" border="1" bordercolor="#c7e1f5" cellspacing="0"> '
        for content in contents:
            # 拼接每个内容
            table_data += str(content)
        table_data += '</table>'

    print(table_data)


    # step 5: 将课表转换为图片
    # 将table_data渲染为带样式的HTML
    html_content = f'<html><head><style>th{{background: #f3faff;border: solid 1px #c7e1f5;}}</style></head><body><h1 style="text-align:center;">{marjor}第{i}周课表</h1>{table_data}</body></html>'

    # 配置imgkit
    config = imgkit.config(
        wkhtmltoimage=r'E:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe')

    # 配置图片大小
    options = {
        'format': 'png',
        'width': 2000,
        'height': 1600,
        # 设置图片质量
        'quality': 100
        # 设置图片的字体

    }

    # 将HTML内容转换为图片
    # 先检查文件夹是否存在，如果不存在，则创建文件夹
    
    if not os.path.exists('E:/编程/python/爬虫/爬取课表/课表/' + marjor + '/'):
        os.makedirs('E:/编程/python/爬虫/爬取课表/课表/' + marjor + '/')

    imgkit.from_string(html_content, 'E:/编程/python/爬虫/爬取课表/课表/' + marjor + '/' + str(i) + '.png', config=config)

    # step 6: 压缩图片大小，不改变图片长宽
    # 打开图片
    img = Image.open('E:/编程/python/爬虫/爬取课表/课表/' + marjor + '/' + str(i) + '.png')

    # 获取图片的宽度和高度
    width, height = img.size

    # 创建一个新的图片对象
    new_img = Image.new('RGB', (width, height), (255, 255, 255))

    # 将图片对象画到新的图片对象上
    new_img.paste(img, (0, 0))

    

    # 保存图片
    new_img.save('E:/编程/python/爬虫/爬取课表/课表/' + marjor + '/' + str(i) + '.png', quality=100)


    # 在图片右上角写上打上水印：陈胜意
    # 打开图片
    img = Image.open('E:/编程/python/爬虫/爬取课表/课表/' + marjor + '/' + str(i) + '.png')

    # 获取图片的宽度和高度
    width, height = img.size

    # 创建一个新的图片对象
    new_img = Image.new('RGB', (width, height), (255, 255, 255))

    # 将图片对象画到新的图片对象上
    new_img.paste(img, (0, 0))

    # 在图片上写上水印
    draw = ImageDraw.Draw(new_img)

    # 设置字体
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 15)

    # 设置水印的位置
    position = (width - 100, 0)

    # 设置水印的内容
    string = 'By：Chensy'

    # 设置水印的颜色
    color = (60, 59, 60)

    # 写上水印
    draw.text(position, string, color, font=font)

    # 保存图片
    new_img.save('E:/编程/python/爬虫/爬取课表/课表/' + marjor + '/' + str(i) + '.png', quality=100)

