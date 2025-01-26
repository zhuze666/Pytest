import hashlib

class DebugTalk:
    def __init__(self):
        self.read = ReadYamlData()
        self.get_data = GetData()
        self.md5 = hashlib.md5()

    def get_data(self, key, random=None):
        """
        获取extract.yaml数据
        :param key: extract.yaml中的key值
        :param random: int类型，0：随机读取；-1：读取全部，返回字符串形式；-2：读取全部，返回列表形式；其他根据列表索引取值，取第一个值为1，第二个为2，以此类推;
        :return:
        """
        # 获取extract.yaml数据
        yaml_data = self.read.get_yaml_data('extract.yaml')
        # 获取yaml_data中key的值
        data = yaml_data.get(key)
        if data is None:
            return None
        # 如果random为0，返回一个随机值
        if random == 0:
            return random.choice(data)
        # 如果random为-1，返回所有值
        elif random == -1:
            return str(data)
         # 如果random为-2，返回所有值并转换为列表
        elif random == -2:
            return data

    #入参生成md5
    def md5(self, params):
        """参数MD5加密"""
        enc_data = hashlib.md5()
        # 获取待输出数据
        enc_data.update(params.encode(encoding="utf-8"))
        return enc_data.hexdigest()
