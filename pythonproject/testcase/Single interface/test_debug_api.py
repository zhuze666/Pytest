import os

import allure
import pytest

from pythonproject.common.readyaml import get_testcase_yaml
from pythonproject.base.apiutil import RequestBase
from pythonproject.base.generateId import m_id, c_id


#m_id是generateId.py生成模块编号的迭代器
@allure.feature(next(m_id) + '用户管理模块（单接口）')
class TestUserManager(object):

    # 场景，allure报告的目录结构
    #c_id是generateId.py生成用例编号的迭代器
    @allure.story(next(c_id) + "新增用户")
    # 测试用例执行顺序设置
    @pytest.mark.run(order=1)
    # 参数化，通过yaml文件中的base_info和testcase参数，执行用例
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/Single interface/addUser.yaml"))
    def test_add_user(self, base_info, testcase):
        # 从 testcase 字典中获取 'case_name' 字段的值，将其设置为当前测试用例在 allure 报告中的标题
        # 这样在生成的 allure 报告中，每个测试用例就会以其对应的用例名称来展示，方便测试人员查看和分析
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "修改用户")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/Single interface/updateUser.yaml"))
    def test_update_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "删除用户")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/Single interface/deleteUser.yaml"))
    def test_delete_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "查询用户")
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/Single interface/queryUser.yaml"))
    def test_query_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)
