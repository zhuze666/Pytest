import sys
import traceback

# sys.path.insert(0, "..")

import configparser
from conf import setting
from common.recordlog import logs


class OperationConfig:
    """封装读取*.ini配置文件模块"""

    def __init__(self, filepath=None):

        '''
        这段代码是OperationConfig类的构造函数，主要功能如下：
        初始化配置文件路径：如果传入的filepath为None，则使用默认路径；否则使用传入的路径。
        使用configparser读取配置文件，捕获并记录可能的异常。获取报告类型。
        '''

    if filepath is None:
        self.__filepath = setting.FILE_PATH['CONFIG']   # 赋值配置文件路径
    else:
        self.__filepath = filepath  # 赋值配置文件路径

    self.conf = configparser.ConfigParser() # 创建一个ConfigParser对象
    try:
        self.conf.read(self.__filepath, encoding='utf-8') # 读取ini配置文件
    except Exception as e:
        exc_type, exc_value, exc_obj = sys.exc_info() # 获取异常类型、异常值和异常对象
        logs.error(str(traceback.print_exc(exc_obj)))

    self.type = self.get_report_type('type') # 获取报告类型


def get_item_value(self, section_name):
    """
    该函数 get_item_value 根据传入的 section_name 参数，从配置文件中获取指定部分的所有键值对，并以字典形式返回。具体步骤如下：
    调用 self.conf.items(section_name) 获取指定部分的所有键值对。将获取到的键值对转换为字典并返回。
    :param section_name: 根据ini文件的头部值获取全部值
    :return:以字典形式返回
    """
    items = self.conf.items(section_name) # 获取指定部分的所有键值对并转换为列表
    return dict(items)


def get_section_for_data(self, section, option):
    """
    该函数用于从ini文件中获取指定section和option的值。如果获取成功则返回值，否则记录错误日志并返回空字符串。
    :param section: ini文件头部值
    :param option:头部值下面的选项
    :return:
    """
    try:
        values = self.conf.get(section, option) # 获取指定section和option的值
        return values
    except Exception as e:
        logs.error(str(traceback.format_exc()))
        return ''


def write_config_data(self, section, option_key, option_value):
    """
    该函数用于将数据写入ini配置文件中。具体功能如下：
    检查指定的section是否存在，如果不存在则添加section并设置option_key和option_value。
    如果section已存在，则记录日志提示写入失败。
    最后将修改后的配置写入文件。
    写入数据到ini配置文件中
    :param section: 头部值
    :param option_key: 选项值key
    :param option_value: 选项值value
    :return:
    """
    if section not in self.conf.sections(): # 判断section是否存在
        # 添加一个section值
        self.conf.add_section(section)  # 若section不存在，添加section
        self.conf.set(section, option_key, option_value)    # 若section存在，设置option_key和option_value
    else:
        logs.info('"%s"值已存在，写入失败' % section)
    with open(self.__filepath, 'w', encoding='utf-8') as f:
        self.conf.write(f)


def get_section_mysql(self, option):
    '''
    该函数 get_section_mysql 接收一个参数 option，并调用类的另一个方法 get_section_for_data，
    传入固定字符串 "MYSQL" 和参数 option，最终返回该方法的结果。
    '''
    return self.get_section_for_data("MYSQL", option)


def get_section_redis(self, option):
    return self.get_section_for_data("REDIS", option)


def get_section_clickhouse(self, option):
    return self.get_section_for_data("CLICKHOUSE", option)


def get_section_mongodb(self, option):
    return self.get_section_for_data("MongoDB", option)


def get_report_type(self, option):
    return self.get_section_for_data('REPORT_TYPE', option)


def get_section_ssh(self, option):
    return self.get_section_for_data("SSH", option)
