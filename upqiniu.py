# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time    : 2018/5/30 18:46
# @Author  : glc

import glob2
import os

from bs4 import BeautifulSoup as bs
from qiniu import Auth, put_file

access_key = 'TECefRZTl1J55HRoGTyt2uMc4GJX-CRuxf39miKu'
secret_key = '5uBOUEoo2WkHdiDK4fmEyxJ6re2-X0OTooq6VTjh'

q = Auth(access_key, secret_key)

bucket_name = 'robo-fff-roboshop2-js'

resources = glob2.glob('dist/static/js/*.js')


def upload(path):
    file_name = path.replace('dist/static/js/', '')
    key = file_name
    token = q.upload_token(bucket_name, key, 3600)
    localfile = './' + path
    put_file(token, key, localfile)


for r in resources:
    if os.path.isfile(r) and r.count('app') or r.count('vendor'):
        upload(r)

""" 以上为上传文件 """

soup = bs(open("dist/index.html", encoding='utf8'), "html.parser")

host = 'http://p9j715g1v.bkt.clouddn.com/'

infos = soup.find_all('script')
for i in infos:
    if 'app' in str(i.attrs.get('src', '')):
        i.attrs['src'] = host + i.attrs['src'][11:]
        print(i, '修改了?')
    elif 'vendor' in str(i.attrs.get('src', '')):
        i.attrs['src'] = host + i.attrs['src'][11:]
    print(i, '修改了?')

with open('dist/index.html', 'w+', encoding='utf8') as d:
    d.write(soup.prettify())
    d.flush()

with open('dist/index.html', 'r', encoding='utf8') as dean:
    print(dean.read())
