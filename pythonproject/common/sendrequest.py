from __future__ import division
from builtins import object
from past.utils import old_div
import json
import allure
import pytest
import requests
import urllib3
import time

from pythonproject.conf import setting
from pythonproject.common.recordlog import logs
from requests import utils
from pythonproject.common.readyaml import ReadYamlData
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class SendRequest(object):
    """发送接口请求，暂时只写了get和post方法的请求"""

    def __init__(self, cookie=None):
        self.cookie = cookie
        self.read = ReadYamlData()

    def get(self, url, data, header):
        """
        :param url: 接口地址
        :param data: 请求参数
        :param header: 请求头
        :return:
        """
        requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            if data is None:
                response = requests.get(url, headers=header, cookies=self.cookie, verify=False)
            else:
                response = requests.get(url, data, headers=header, cookies=self.cookie, verify=False)
        except requests.RequestException as e:
            logs.error(e)
            return None
        except Exception as e:
            logs.error(e)
            return None
        # 响应时间/毫秒
        res_ms = old_div(response.elapsed.microseconds, 1000)
        # 响应时间/秒
        res_second = response.elapsed.total_seconds()
        response_dict = dict()

        # 接口响应状态码
        response_dict['code'] = response.status_code
        # 接口响应文本
        response_dict['text'] = response.text
        try:
            response_dict['body'] = response.json().get('body')
        except Exception:
            response_dict['body'] = ''
        response_dict['res_ms'] = res_ms
        response_dict['res_second'] = res_second
        return response_dict

    def post(self, url, data, header):
        """
        :param url:
        :param data: verify=False忽略SSL证书验证
        :param header:
        :return:
        """
        # 控制台输出InsecureRequestWarning错误
        requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            if data is None:
                response = requests.post(url, header, cookies=self.cookie, verify=False)
            else:
                response = requests.post(url, data, headers=header, cookies=self.cookie, verify=False)
        except requests.RequestException as e:
            logs.error(e)
            return None
        except Exception as e:
            logs.error(e)
            return None
        # 响应时间/毫秒
        res_ms = old_div(response.elapsed.microseconds, 1000)
        # 响应时间/秒
        res_second = response.elapsed.total_seconds()
        response_dict = dict()
        # 接口响应状态码
        response_dict['code'] = response.status_code
        # 接口响应文本
        response_dict['text'] = response.text
        try:
            response_dict['body'] = response.json().get('body')
        except Exception:
            response_dict['body'] = ''
        response_dict['res_ms'] = res_ms
        response_dict['res_second'] = res_second
        return response_dict

    def send_request(self, **kwargs):
        """
        发送HTTP请求并处理响应结果。

        使用requests库创建一个会话，并用该会话发送请求。本函数主要负责处理HTTP请求的发送和响应结果的处理，
        包括异常处理和Cookie的保存。

        参数:
        **kwargs: 关键字参数，包含请求所需的参数，如url、method等。

        返回:
        requests.Response: 返回请求的响应结果，包含响应内容、状态码等信息。
        """

        # 创建一个requests会话
        session = requests.session()
        result = None
        cookie = {}
        try:
            # 发送请求
            result = session.request(**kwargs)   #**kwargs 是一个字典，包含了请求所需的参数，如url、method等。
            # 将响应中的Cookies转换为字典
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookie:
                # 将Cookies保存到Cookie字典中
                cookie['Cookie'] = set_cookie
                # 将Cookie信息写入YAML文件
                self.read.write_yaml_data(cookie)
                # 记录日志，打印接口返回的信息
                logs.info("cookie：%s" % cookie)
            logs.info("接口返回信息：%s" % result.text if result.text else result)
        except requests.exceptions.ConnectionError:
            # 处理连接异常
            logs.error("ConnectionError--连接异常")
            # 断言失败，在allure报告中抛出异常，否则会按执行通过处理
            pytest.fail("接口请求异常，可能是request的连接数过多或请求速度过快导致程序报错！")
        except requests.exceptions.HTTPError:
            # 处理HTTP异常
            logs.error("HTTPError--http异常")
        except requests.exceptions.RequestException as e:
            # 处理其他请求异常
            logs.error(e)
            pytest.fail("请求异常，请检查系统或数据是否正常！")
        return result

    def run_main(self, name, url, case_name, header, method, cookies=None, file=None, **kwargs):
        """
        接口请求
        :param name: 接口名
        :param url: 接口地址
        :param case_name: 测试用例
        :param header:请求头
        :param method:请求方法
        :param cookies：默认为空
        :param file: 上传文件接口
        :param kwargs: 请求参数，根据yaml文件的参数类型，一般可能为data、json，params
        :return:
        """

        try:
            # 收集报告日志
            logs.info('接口名称：%s' % name)
            logs.info('请求地址：%s' % url)
            logs.info('请求方式：%s' % method)
            logs.info('测试用例名称：%s' % case_name)
            logs.info('请求头：%s' % header)
            logs.info('Cookie：%s' % cookies)
            # 处理请求参数
            req_params = json.dumps(kwargs, ensure_ascii=False)# json.dump(）用于数据序列化，将传入的关键字参数字典转换为JSON格式的字符串
            if "data" in list(kwargs.keys()):
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
            elif "json" in list(kwargs.keys()):
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
            elif "params" in list(kwargs.keys()):
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
        except Exception as e:
            logs.error(e)
        # time.sleep(0.5)
        # 控制台输出InsecureRequestWarning错误
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        # 发送请求
        response = self.send_request(method=method,
                                     url=url,
                                     headers=header,
                                     cookies=cookies,
                                     files=file,
                                     timeout=setting.API_TIMEOUT,
                                     verify=False,
                                     **kwargs)
        return response
