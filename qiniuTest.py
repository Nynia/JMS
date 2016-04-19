# -*- coding: utf-8 -*-
# flake8: noqa
import os
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
access_key = 'jJnJu4_d7YH8hhhB-J4J8Jr537T_-yk9BIsin75M'
secret_key = 'WpidgDmScl866DLV22LT2Qon19oDkiLmRbxhDrGq'

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'head'

#上传到七牛后保存的文件名
key = 'my-python-logo2.png'

#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

#要上传文件的本地路径
localfile = "\\0001.jpg"
print os.getcwd()

ret, info = put_file(token, key, localfile)
print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)