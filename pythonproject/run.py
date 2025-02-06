import os
import shutil
import webbrowser

import pytest

from conf.setting import REPORT_TYPE

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
        '''
        pytest.main(
            ['-s', '-v', '--alluredir=./report/temp', './testcase', '--clean-alluredir',
             '--junitxml=./report/results.xml'])

        shutil.copy('./environment.xml', './report/temp')
        os.system(f'allure serve ./report/temp')

    elif REPORT_TYPE == 'tm':
        pytest.main(['-vs', '--pytest-tmreport-name=testReport.html', '--pytest-tmreport-path=./report/tmreport'])
        webbrowser.open_new_tab(os.getcwd() + '/report/tmreport/testReport.html')
