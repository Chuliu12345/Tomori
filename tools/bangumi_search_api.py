import requests
import json
import os
from dotenv import load_dotenv
try:
    from tools.tool import tool
except ModuleNotFoundError:
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

@tool
def search_subjects(subject, limit=3, offset=0):
    """
    搜索条目
    :param type: 条目类型,不使用为全部类型，2为动漫
    """
    url = f"{public_server}/search/subjects"
    params = {
        "limit": limit,
        "offset": offset,
    }
    payload = {
        "keyword": subject,
        "filter": {
            "type": [2],
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
