
#解析${}.yaml中${}包含的数据并取出
def extract_data(yaml_file_path, key):
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        # 正则匹配${key}
        pattern = r'\$\{(.+?)\}'
        matches = re.findall(pattern, data[key])
        for match in matches:
            # 获取yaml中${key}的数据
            value = data.get(match)
            if value:
                data[key] = value
    return data


