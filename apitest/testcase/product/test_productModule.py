import allure
import pytest

from base.apiutil import RequestBase
from base.generateId import m_id, c_id
from common.operyaml import get_testcase_yaml


@allure.feature(next(m_id) + '电子商务管理系统接口')
class TestProductModule:

    @allure.story(next(c_id) + "获取商品列表")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("/apitest/testcase/product/getProductList.yaml"))
    def test_product_list(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)