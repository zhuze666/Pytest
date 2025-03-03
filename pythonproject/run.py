from __future__ import absolute_import
import os
import shutil
import webbrowser
import allure
import pytest
import logging

from pythonproject.conf.setting import REPORT_TYPE

if __name__ == '__main__':

    if REPORT_TYPE == 'allure':
        '''
        -v, --verbose: 增加输出详细度。
        -q, --quiet: 减少输出信息。
        -s: 输出调试信息，包括print()的
        -x, --exitfirst: 遇到第一个失败就退出。
        --maxfail = < num >: 失败数量达到指定值后退出。
        -k < expr >: 根据测试名称表达式选择测试。
        -m < markexpr >: 根据标记表达式选择测试。
        --tb = {auto, long, short, no}: 控制回溯格式。
        -n < numprocesses >: 使用多个进程并行运行测试。
        --cov = < path >: 启用覆盖率报告。
        --html = < path >: 生成HTML格式的测试报告。
        -- alluredir=./report/temp：将测试执行过程中的数据保存到这个目录中，以便后续生成 Allure 报告
        --./testcase： 在这个目录下查找所有符合测试用例命名规则的文件并执行其中的测试用例
        --clean-alluredir： 在生成 Allure 报告之前，先清空指定的 --alluredir 目录
        --junitxml=./report/results.xml： 指定生成 JUnit 格式的测试报告文件为 ./report/results.xml
        '''



        pytest.main(
            ['-s', '-v', '--alluredir=./report/temp', './testcase', '--clean-alluredir',
             '--junitxml=./report/results.xml'])
        # 使用 shutil 库的 copy 函数将当前目录下的 environment.xml 文件复制到 ./report/temp 目录中
        # environment.xml 文件通常包含 Allure 报告所需的环境信息
        if os.path.exists('./environment.xml'):
            shutil.copy('./environment.xml', './report/temp')
        else:
            print("environment.xml 文件不存在，跳过复制操作。")

        # 该命令会启动 Allure 服务器并将 ./report/temp 目录中的数据生成 Allure 报告
        # 然后在浏览器中打开报告页面
        os.system(f'allure serve ./report/temp')

    # 如果是tm，则执行 pytest-tmreport 报告生成逻辑
    elif REPORT_TYPE == 'tm':
        '''
        --vs: 表示以详细模式运行测试并不捕获标准输出
        --pytest-tmreport-name=testReport.html: 指定 pytest-tmreport 插件生成的 HTML 测试报告的文件名为 testReport.html
        --pytest-tmreport-path=./report/tmreport: 指定 pytest-tmreport 插件生成的 HTML 测试报告的存储目录为 ./report/tmreport
        '''
        pytest.main(['-vs', '--pytest-tmreport-name=testReport.html', '--pytest-tmreport-path=./report/tmreport'])
        # 使用 webbrowser 库的 open_new_tab 函数在浏览器中打开一个新的标签页
        # os.getcwd() 返回当前工作目录的路径,拼接出 HTML 测试报告的完整路径，然后在浏览器中打开该报告
        webbrowser.open_new_tab(os.getcwd() + '/report/tmreport/testReport.html')
