# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
import time

import pytest

from pythonproject.common.readyaml import ReadYamlData
from pythonproject.base.removefile import remove_file
from pythonproject.common.dingRobot import send_dd_msg
from pythonproject.conf.setting import dd_msg

import warnings

yfd = ReadYamlData()

#@pytest.fixture代表用例前置处理器，该函数在测试会话开始前执行一次。
#scope代表作用域
@pytest.fixture(scope="session", autouse=True)
def clear_extract():
    """
    清理环境的fixture函数，自动在测试会话开始前执行一次。

    该函数主要进行测试前的环境清理工作，包括忽略特定警告和清理之前的测试数据文件。
       """
    # 禁用HTTPS告警，ResourceWarning
    warnings.simplefilter('ignore', ResourceWarning)

    ## 清理之前的测试数据
    yfd.clear_yaml_data()
    # 删除报告临时目录下的指定类型文件
    remove_file("./report/temp", ['json', 'txt', 'attach', 'properties'])


def generate_test_summary(terminalreporter):
    """生成测试结果摘要字符串"""
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    duration = time.time() - terminalreporter._sessionstarttime

    summary = f"""
    自动化测试结果，通知如下，请着重关注测试失败的接口，具体执行结果如下：
    测试用例总数：{total}
    测试通过数：{passed}
    测试失败数：{failed}
    错误数量：{error}
    跳过执行数量：{skipped}
    执行总时长：{duration}
    """
    print(summary)
    return summary


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """自动收集pytest框架执行的测试结果并打印摘要信息"""
    summary = generate_test_summary(terminalreporter)
    if dd_msg:
        send_dd_msg(summary)
