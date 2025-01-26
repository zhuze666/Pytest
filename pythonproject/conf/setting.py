import logging
import os
import sys

DIR_BASE = os.path.dirname(os.path.dirname(__file__)) # 项目根目录
sys.path.append(DIR_BASE) # 加入项目根目录到sys.path中

# log日志输出级别
LOG_LEVEL = logging.DEBUG  # 文件
STREAM_LOG_LEVEL = logging.DEBUG  # 控制台

# 接口超时时间，单位/s
API_TIMEOUT = 60

# excel文件的sheet页，默认读取第一个sheet页的数据，int类型，第一个sheet为0，以此类推0.....9
SHEET_ID = 0

# 生成的测试报告类型，可以生成两个风格的报告，allure或tm
REPORT_TYPE = 'allure'

# 是否发送钉钉消息
dd_msg = False

# 文件路径
FILE_PATH = {
    'CONFIG': os.path.join(DIR_BASE, 'conf/config.ini'), # 配置文件路径
    'LOG': os.path.join(DIR_BASE, 'logs'), # 日志路径
    'YAML': os.path.join(DIR_BASE), # yaml路径
    'TEMP': os.path.join(DIR_BASE, 'report/temp'), # 临时报告路径
    'TMR': os.path.join(DIR_BASE, 'report/tmreport'), # 团队报告路径
    'EXTRACT': os.path.join(DIR_BASE, 'extract.yaml'), # 扩展数据路径
    'XML': os.path.join(DIR_BASE, 'data/sql'), # sql路径
    'RESULTXML': os.path.join(DIR_BASE, 'report'), # 结果报告路径
    'EXCEL': os.path.join(DIR_BASE, 'data', '测试数据.xls') # 原始excel路径
}

# 默认请求头信息
LOGIN_HEADER = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive'
}
