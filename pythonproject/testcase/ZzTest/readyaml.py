from __future__ import print_function
from __future__ import absolute_import
import os
import json
import yaml
from . import debugTalk


# 读取yaml文件中的数据
def read_yaml(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
            return yaml_data
    except Exception as e:
        print(e)

#读取yaml文件中指定key字段的value值
def get_yaml_value(file, key):
    #先判断extract.ymal文件是否存在,如果不存在就创建一个
        if not os.path.exists(file):
            os.system(file)
        yaml_data = read_yaml(file)
        if key in yaml_data:
            return yaml_data[key]
        else:
            print(f'在 {file} 中找不到键为 {key} 的值')
            return None



# 把数据写入yaml文件
"""def write_yaml(file, file_path):
    file = None
    file_path = r'extract.yaml'
    if not os.path.exists(file_path):
        os.system(file_path)
    try:
        with open(file, 'w', encoding='utf-8') as file:
            write_data = yaml.dump(data, allow_unicode=True, sort_keys=False)
            file.write(write_data)
    except Exception as e:
        print(e)"""


def write_yaml(data, file_path):
    """
    将字典数据写入指定的 YAML 文件。

    :param data: 要写入的数据，必须是字典类型。
    :param file_path: 目标 YAML 文件的路径。
    """
    try:
        # 检查文件路径是否为空或 None
        if not file_path:
            raise ValueError("File path cannot be empty or None.")

        # 检查数据是否为字典类型
        if not isinstance(data, dict):
            print('写入到 [{}] 的数据必须是字典类型格式！'.format(file_path))
            return

        # 确保文件夹存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 写入数据到文件
        with open(file_path, mode='a', encoding='utf-8') as file:
            write_data = yaml.dump(data, allow_unicode=True, sort_keys=False)
            file.write(write_data)
        print(f"数据已成功写入到 [{file_path}]")
    except Exception as e:
        print(f"写入 [{file_path}] 时发生错误: {e}")


if __name__ == '__main__':
    data = read_yaml('extract.yaml')
    #获取extract.yaml的token字段的value值
    token = get_yaml_value('extract.yaml', 'token')
    print(token)
    #讲token进行md5加密
    md5_token = debugTalk.DebugTalk.md5('token', token)
    print(md5_token)
    #把token的键值对写入到test.yaml中,需要把数值加个key
    Token_dict = {'token': md5_token}
    write_yaml(Token_dict, './test.yaml')
    #获取login.yaml文件的
    #测试代码是否一致

