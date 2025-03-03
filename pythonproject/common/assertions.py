from builtins import str
from builtins import object
import traceback
import allure
import jsonpath
import operator

from pythonproject.common.recordlog import logs
from pythonproject.common.connection import ConnectMysql


class Assertions(object):
    """"
    接口断言模式，支持
    1）响应文本字符串包含模式断言
    2）响应结果相等断言
    3）响应结果不相等断言
    4）响应结果任意值断言
    5）数据库断言

    """

    def contains_assert(self, value, response, status_code):
        """
        1）响应文本字符串包含模式断言模式：断言预期结果的字符串是否包含在接口的响应信息中
        :param value: 预期结果，yaml文件的预期结果值
        :param response: 接口实际响应结果
        :param status_code: 响应状态码
        :return: 返回结果的状态标识
        """
        # 初始化一个标志变量，用于记录断言失败的次数（0代表成功，其他都代表失败）
        flag = 0
        # 遍历yaml文件中预期结果字典中的每一项
        for assert_key, assert_value in list(value.items()):
            # 如果断言键是状态码
            if assert_key == "status_code":
                # 如果预期状态码与实际状态码不匹配
                if assert_value != status_code:
                    # 断言失败次数加1
                    flag += 1
                    # 使用allure报告附件功能记录断言失败信息
                    allure.attach(f"预期结果：{assert_value}\n实际结果：{status_code}", '响应代码断言结果:失败',
                                  attachment_type=allure.attachment_type.TEXT)
                    # 记录错误日志
                    logs.error("contains断言失败：接口返回码【%s】不等于【%s】" % (status_code, assert_value))
            # 如果当前项不是断言状态码，则进行字符串包含断言
            else:
                # 使用jsonpath表达式从响应结果中提取对应键的值，结果是一个列表
                resp_list = jsonpath.jsonpath(response, "$..%s" % assert_key)
                # 判断提取的第一个元素是字符串列表，如果是，就将所有元素拼成一个字符串重新赋值给resp_list
                if isinstance(resp_list[0], str):
                    resp_list = ''.join(resp_list)
                # 如果提取到了值（即列表不为空）
                if resp_list:
                    # 处理断言值中的'NONE'，转换为None
                    assert_value = None if assert_value.upper() == 'NONE' else assert_value
                    # 如果断言值在提取的结果中
                    if assert_value in resp_list:
                        # 记录断言成功日志
                        logs.info("字符串包含断言成功：预期结果【%s】,实际结果【%s】" % (assert_value, resp_list))
                    else:
                        # 断言失败次数加1
                        flag = flag + 1
                        # 记录断言失败的详细信息
                        allure.attach(f"预期结果：{assert_value}\n实际结果：{resp_list}", '响应文本断言结果：失败',
                                      attachment_type=allure.attachment_type.TEXT)
                        logs.error("响应文本断言失败：预期结果为【%s】,实际结果为【%s】" % (assert_value, resp_list))
        # 返回标识，只有0是断言成功
        return flag

    def equal_assert(self, expected_results, actual_results, statuc_code=None):
        """
        2）响应结果相等断言模式
        :param expected_results: 预期结果，yaml文件validation值
        :param actual_results: 接口实际响应结果
        :return:
        """
        flag = 0
        # 检查actual_results和expected_results是否都是字典类型
        if isinstance(actual_results, dict) and isinstance(expected_results, dict):
            # 找出实际结果与预期结果共同的key，注意：这里的逻辑只会获取第一个共同key，如果有多个则忽略其他
            common_keys = list(list(expected_results.keys()) & list(actual_results.keys()))[0]
            # 根据相同的key去实际结果中获取，并重新生成一个实际结果的字典，这里只考虑了单个共同key的情况
            new_actual_results = {common_keys: actual_results[common_keys]}
            # 使用python的内置函数operator.eq进行比较，这里只比较单个共同key的情况
            eq_assert = operator.eq(new_actual_results, expected_results)
            # 如果相等，则记录成功日志，并使用allure附加成功信息
            if eq_assert:
                logs.info(f"相等断言成功：接口实际结果：{new_actual_results}，等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{new_actual_results}", '相等断言结果：成功',
                              attachment_type=allure.attachment_type.TEXT)
            # 如果不相等，则增加flag值，记录错误日志，并使用allure附加失败信息
            else:
                flag += 1
                logs.error(f"相等断言失败：接口实际结果{new_actual_results}，不等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{new_actual_results}", '相等断言结果：失败',
                              attachment_type=allure.attachment_type.TEXT)
        # 如果actual_results或expected_results不是字典类型，则抛出TypeError异常
        else:
            raise TypeError('相等断言--类型错误，预期结果和接口实际响应结果必须为字典类型！')
        # 返回flag值，表示断言是否失败
        return flag

    def not_equal_assert(self, expected_results, actual_results, statuc_code=None):
        """
        3）响应结果不相等断言模式
        :param expected_results: 预期结果，yaml文件validation值
        :param actual_results: 接口实际响应结果
        :return:
        """
        flag = 0
        if isinstance(actual_results, dict) and isinstance(expected_results, dict):
            # 找出实际结果与预期结果共同的key
            common_keys = list(list(expected_results.keys()) & list(actual_results.keys()))[0]
            # 根据相同的key去实际结果中获取，并重新生成一个实际结果的字典
            new_actual_results = {common_keys: actual_results[common_keys]}
            eq_assert = operator.ne(new_actual_results, expected_results)
            if eq_assert:
                logs.info(f"不相等断言成功：接口实际结果：{new_actual_results}，不等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{new_actual_results}", '不相等断言结果：成功',
                              attachment_type=allure.attachment_type.TEXT)
            else:
                flag += 1
                logs.error(f"不相等断言失败：接口实际结果{new_actual_results}，等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{new_actual_results}", '不相等断言结果：失败',
                              attachment_type=allure.attachment_type.TEXT)
        else:
            raise TypeError('不相等断言--类型错误，预期结果和接口实际响应结果必须为字典类型！')
        return flag

    def assert_response_any(self, actual_results, expected_results):
        """
        4）断言接口响应信息中的body的任何属性值
        :param actual_results: 接口实际响应信息
        :param expected_results: 预期结果，在接口返回值的任意值
        :return: 返回标识,0表示测试通过，非0则测试失败
        """
        flag = 0
        try:
            exp_key = list(expected_results.keys())[0]
            if exp_key in actual_results:
                act_value = actual_results[exp_key]
                rv_assert = operator.eq(act_value, list(expected_results.values())[0])
                if rv_assert:
                    logs.info("响应结果任意值断言成功")
                else:
                    flag += 1
                    logs.error("响应结果任意值断言失败")
        except Exception as e:
            logs.error(e)
            raise
        return flag

    def assert_response_time(self, res_time, exp_time):
        """
        通过断言接口的响应时间与期望时间对比,接口响应时间小于预期时间则为通过
        :param res_time: 接口的响应时间
        :param exp_time: 预期的响应时间
        :return:
        """
        try:
            assert res_time < exp_time
            return True
        except Exception as e:
            logs.error('接口响应时间[%ss]大于预期时间[%ss]' % (res_time, exp_time))
            raise

    def assert_mysql_data(self, expected_results):
        """
        5）数据库断言
        :param expected_results: 预期结果，yaml文件的SQL语句
        :return: 返回flag标识，0表示正常，非0表示测试不通过
        """
        flag = 0
        conn = ConnectMysql()
        # 调用 conn 对象的 query_all 方法，传入预期结果对应的 SQL 语句 expected_results
        # 该方法会执行 SQL 查询并返回查询结果
        db_value = conn.query_all(expected_results)
        # 如果查询结果不为 None，说明数据库中存在符合预期的数据
        if db_value is not None:
            logs.info("数据库断言成功")
        else:
            flag += 1
            logs.error("数据库断言失败，请检查数据库是否存在该数据！")
        return flag

    def assert_result(self, expected, response, status_code):
        """
        断言，通过断言all_flag标记，all_flag==0表示测试通过，否则为失败
        :param expected: 预期结果
        :param response: 实际响应结果
        :param status_code: 响应code码
        :return:
        """
        all_flag = 0
        try:
            logs.info("yaml文件预期结果：%s" % expected)
            # logs.info("实际结果：%s" % response)
            # all_flag = 0
            #循环预期结果，进行断言，以上几种模式必须全部断言成功才认为通过
            for yq in expected:
                for key, value in list(yq.items()):
                    #如果key是"contains"，就调用1）响应文本字符串包含模式断言模式：断言预期结果的字符串是否包含在接口的响应信息中
                    if key == "contains":
                        flag = self.contains_assert(value, response, status_code)
                        all_flag = all_flag + flag
                    #如果key是"eq"，就调用2）2）响应结果相等断言模式
                    elif key == "eq":
                        flag = self.equal_assert(value, response)
                        all_flag = all_flag + flag
                    #如果key是"ne"，就调用3）响应结果不相等断言模式
                    elif key == 'ne':
                        flag = self.not_equal_assert(value, response)
                        all_flag = all_flag + flag
                    #如果key是"rv"，就调用4）响应结果任意值断言模式
                    elif key == 'rv':
                        flag = self.assert_response_any(actual_results=response, expected_results=value)
                        all_flag = all_flag + flag
                    #如果key是"db"，就调用5）数据库断言模式
                    elif key == 'db':
                        flag = self.assert_mysql_data(value)
                        all_flag = all_flag + flag
                    else:
                        logs.error("不支持此种断言方式")

        except Exception as exceptions:
            logs.error('接口断言异常，请检查yaml预期结果值是否正确填写!')
            # raise exceptions 会导致抛出异常，不会执行后续的代码，暂时不使用
            #raise exceptions

        if all_flag == 0:
            logs.info("测试成功")
            assert True
        else:
            logs.error("测试失败")
            assert False
