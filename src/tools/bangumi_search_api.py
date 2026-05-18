import requests
import json
import os
from dotenv import load_dotenv

# 支持两种运行方式：作为模块和作为脚本
try:
    from .tool import tool # 直接作为脚本运行时，相对导入会失败
except ImportError:
    from tool import tool


public_server = "https://api.bgm.tv/v0"
private_server = "https://next.bgm.tv/p1"
load_dotenv()

access_token = os.getenv("bangumi_acg_agent_token")
private_headers = {
        # 设置一个规范的用户代理，这是 Bangumi API 的建议，有助于提高请求的成功率和稳定性
        "User-Agent": "mytomori/1.0 (https://github.com/yourusername/your-repo)",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer 23{access_token}"
    }
public_headers = {
        # 设置一个规范的用户代理，这是 Bangumi API 的建议，有助于提高请求的成功率和稳定性
        "User-Agent": "mytomori/1.0 (https://github.com/yourusername/your-repo)",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
print(access_token)

@tool(description="如果明确只需要搜索番剧/动漫条目，anime_only=True，其他情况不传或传False")
def search_subjects(subject, anime_only=False, limit=3, offset=0):
    """
    搜索番剧条目(ONLY传入subject参数，除非需要更多结果)
    :param subject: 【必需】番剧名称关键词
    :param limit: 【可选，默认3】结果数量限制。仅当首次搜索结果不足以找到目标时使用。通常不传。
    :param offset: 【可选，默认0】分页偏移量。仅在扩展搜索时使用。通常不传。
    """
    url = f"{public_server}/search/subjects"
    params = {
        "limit": limit,
        "offset": offset,
    }
    if anime_only:
        payload = {
            "keyword": subject,
            "filter": {
                "type": [2],
                "nsfw": True
            }
        }
    else:
        payload = {
            "keyword": subject,
            "filter": {
                "nsfw": True
            }
        }
    data = []
    try:
        resp = requests.post(url, headers=public_headers, params=params, json=payload, timeout=10)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message
@tool(description="动漫角色(虚拟人物)")
def search_characters(character_name, limit=3, offset=0):
    url = f"{public_server}/search/characters"
    params = {
        "limit": limit,
        "offset": offset,
    }
    payload = {
        "keyword": character_name,
        "filter": {
            "nsfw": True
        }
    }
    data = []
    try:
        resp = requests.post(url, headers=public_headers, params=params, json=payload, timeout=10)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message

@tool(description="搜索人物条目，人物为现实世界中的人物")
def search_persons(person_name, limit=3, offset=0):
    url = f"{public_server}/search/persons"
    params = {
        "limit": limit,
        "offset": offset,
    }
    payload = {
        "keyword": person_name,
        "filter": {
            "nsfw": True
        }
    }
    data = []
    try:
        resp = requests.post(url, headers=public_headers, params=params, json=payload, timeout=10)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message

if __name__ == "__main__":
    print(search_subjects.run({"subject": "上伊那"}))
