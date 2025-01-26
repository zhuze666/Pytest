import requests

url = "http://127.0.0.1:8787/dar/user/login"
url2 = "http://127.0.0.1:8787/dar/user/queryUser"
url3 = "http://127.0.0.1:8787/coupApply/cms/goodsList"

header = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}

data = {
    "user_name": "test01",
    "passwd": "admin123"
}

data2 = {
    "user_id": 123839387391912
}
data3 = {
    "msgType": "getHandsetListOfCust",
    "page": 1,
    "size": 20
}
# 例1：获取用户的token
req = requests.post(url=url, headers=header, data=data)
token = req.json().get("token")
print(req.text)
print(token)

# 例2：共享session
req_session = requests.session()
req2=req_session.request(method="post", url=url2, headers=header,data = data2)
print(req2.text)

# 例3：
req3 = requests.get(url=url3, headers=header, params=data3)
print(req3.text)
