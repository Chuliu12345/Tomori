from typing import Any, Dict, List
def extract_keys(item, keys_dict):
    if not isinstance(keys_dict, dict):
        return item
    result = {}
    for key, value in keys_dict.items():
        if key in item:
            if isinstance(value, dict):
                # 检查item[key]是否是列表（可能包含字典）
                if isinstance(item[key], list):
                    # 对列表中的每个元素处理
                    result[key] = [extract_keys(elem, value) if isinstance(elem, dict) else elem for elem in item[key]]
                else:
                    result[key] = extract_keys(item[key], value)
            else:
                result[key] = item[key]
    return result
def compress_json(data:List[Dict],  keys:Dict)->List:
    """
    压缩 JSON 数据，根据keys的嵌套结构，只保留指定的键
    :param data: 原始 JSON 数据列表
    :param keys: 需要保留的键的嵌套字典结构
    :return: 压缩后的 JSON 数据列表
    """
    compressed_data = []
    for item in data:
        compressed_item = extract_keys(item, keys)
        compressed_data.append(compressed_item)
    return compressed_data

def test():
    # 测试用例1：基础嵌套字典
    data = [
        {
            "id": 1,
            "name": "Alice",
            "age": 30,
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "country": "USA"
            },
            "hobbies": ["reading", "traveling"]
        },
        {
            "id": 2,
            "name": "Bob",
            "age": 25,
            "address": {
                "street": "456 Elm St",
                "city": "Othertown",
                "country": "USA"
            },
            "hobbies": ["sports", "music"]
        }
    ]
    keys = {
        "id": None,
        "name": None,
        "address": {
            "city": None
        }
    }
    compressed_data = compress_json(data, keys)
    print("测试用例1（基础嵌套字典）:")
    print(compressed_data)
    print()
    
    # 测试用例2：包含dict列表的情况
    data2 = [
        {
            "id": 1,
            "name": "Product A",
            "reviews": [
                {"rating": 5, "comment": "Great!", "author": "User1"},
                {"rating": 4, "comment": "Good", "author": "User2"}
            ]
        },
        {
            "id": 2,
            "name": "Product B",
            "reviews": [
                {"rating": 3, "comment": "OK", "author": "User3"},
                {"rating": 4, "comment": "Nice", "author": "User4"}
            ]
        }
    ]
    keys2 = {
        "id": None,
        "name": None,
        "reviews": {
            "rating": None,
            "author": None
        }
    }
    compressed_data2 = compress_json(data2, keys2)
    print("测试用例2（dict组成的list）:")
    print(compressed_data2)
if __name__ == "__main__":
    test()