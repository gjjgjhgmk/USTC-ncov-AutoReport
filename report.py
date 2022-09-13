import time
import re
import argparse
from bs4 import BeautifulSoup
import json
import re
from ustclogin import Login
class Report(object):
    def __init__(self, stuid, password, data_path):
        self.stuid = stuid
        self.password = password
        self.data_path = data_path

    def report(self):
        login=Login(self.stuid,self.password,'https://weixine.ustc.edu.cn/2020/caslogin')
        if login.login():
            data = login.result.text
            data = data.encode('ascii','ignore').decode('utf-8','ignore')
            soup = BeautifulSoup(data, 'html.parser')
            token = soup.find("input", {"name": "_token"})['value']

            with open(self.data_path, "r+", encoding='utf-8') as f:
                data = f.read()
                data = json.loads(data)
                data["_token"]=token
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
            }

            url = "https://weixine.ustc.edu.cn/2020/daliy_report"
            data=login.session.post(url, data=data, headers=headers).text
            soup = BeautifulSoup(data, 'html.parser')
            token = soup.select("p.alert.alert-success")[0]
            flag = False
            if '成功' in token.text:
                flag=True
            headers={
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39'}
            url = "https://weixine.ustc.edu.cn/2020/upload/xcm" #上传两码
            data=login.session.get(url,headers=headers).text
            data = data.encode('ascii','ignore').decode('utf-8','ignore')
            data=re.search(r"formData:{([\s\S]*?)}",data,re.M)
            data='{'+data.group(1)+'}'
            data=data.replace("_token","'token'")
            data=data.replace("'",'"')
            data=json.loads(data)
            data['t']='1' #1是上传行程码，2是上传健康码，3是上传核酸检测报告
            data['id']='WU_FILE_0'
            file={'file':open('trace.jpg','rb')}
            login.session.post('https://weixine.ustc.edu.cn/2020img/api/upload_for_student',headers=headers,data=data,files=file)
            data['t']='2'
            file={'file':open('safe.jpg','rb')}
            login.session.post('https://weixine.ustc.edu.cn/2020img/api/upload_for_student',headers=headers,data=data,files=file)
            data=login.session.get('https://weixine.ustc.edu.cn/2020/apply/daliy',headers=headers).text #报备
            data = data.encode('ascii','ignore').decode('utf-8','ignore')
            soup = BeautifulSoup(data, 'html.parser')
            token = soup.find("input", {"name": "_token"})['value']
            data=login.session.get('https://weixine.ustc.edu.cn/2020/apply/daliy/i?t=3',headers=headers).text
            data = data.encode('ascii','ignore').decode('utf-8','ignore')
            soup = BeautifulSoup(data, 'html.parser')
            start_date = soup.find("input", {"id": "start_date"})['value']
            end_date = soup.find("input", {"id": "end_date"})['value']
            data={
                '_token':token,
                'start_date':start_date,
                'end_date':end_date,
                'return_college[]':'西校区',
                'return_college[]':'中校区',
                'reason':'跨校区上课',
                't':'3'}
            post=login.session.post('https://weixine.ustc.edu.cn/2020/apply/daliy/ipost',data=data)
            if post.url=='\
https://weixine.ustc.edu.cn/2020/apply_total?t=d' and flag==True:
                flag=True
            else:
                flag=False
            if flag == False:
                print("Report FAILED!")
            else:
                print("Report SUCCESSFUL!")
            return flag
        else:
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='URC nCov auto report script.')
    parser.add_argument('data_path', help='path to your own data used for post method', type=str)
    parser.add_argument('stuid', help='your student number', type=str)
    parser.add_argument('password', help='your CAS password', type=str)
    args = parser.parse_args()
    autorepoter = Report(stuid=args.stuid, password=args.password, data_path=args.data_path)
    count = 5
    while count != 0:
        ret = autorepoter.report()
        if ret != False:
            break
        print("Report Failed, retry...")
        count = count - 1
    if count != 0:
        exit(0)
    else:
        exit(-1)
