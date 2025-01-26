import requests


class SendRequests(object):

    def __init__(self):
        pass

    def get(self,url, header, data):
        if header is None:
            res = requests.get(url=url, data=data)
        else:
            res = requests.get(url=url, params=header, data=data)
        return res.json()

    def post(self,url, header, data):
        if header is None:
            res = requests.post(url=url, data=data)
        else:
            res = requests.post(url=url, data=data, headers=header)
        return res.json()

    def run_main(self,url,data,header,method):
        if method.upper() == "GET":
            res = self.get(url=url, header=header, data=data)
        else:
            method.upper() == "POST"
            res =  self.post(url=url, header=header, data=data)
        return res


if __name__ == '__main__':
        url = "http://127.0.0.1:8787/dar/user/login"
        data = {
              "user_name": "test01",
              "passwd": "admin123"
        }
        method="post"
        header = None
        send = SendRequests()
        res = send.run_main(url=url,  data=data,  method=method, header=header)
        print(res)