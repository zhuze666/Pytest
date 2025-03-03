from builtins import str
import pandas as pd
from pythonproject.common.recordlog import logs
import traceback


def read_csv(filepath, col_name):
    """
    功能: 读取 CSV 文件并提取指定列数据
    :param filepath: csv目录
    :param col_name: 取值的列名
    usecols：需要读取的列，可以是列的位置编号，也可以是列的名称
    error_bad_lines = False  当某行数据有问题时，不报错，直接跳过，处理脏数据时使用
    :return:
    """
    try:
        df = pd.read_csv(filepath, encoding="GBK")
        # 提取指定列的数据并转换为列表
        data = df[col_name].tolist()
        return data
    except Exception:
        logs.error(str(traceback.format_exc()))


if __name__ == '__main__':
    filepath = "D:/PycharmProject/pythonproject/data/vehicleNo.csv"
    col_name = "vno"
    data = read_csv(filepath, col_name)
    print(data)