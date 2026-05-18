import requests
import json
import os
from dotenv import load_dotenv

# 支持两种运行方式：作为模块和作为脚本
try:
    from .tool import tool
    from .compress_json import compress_json
except ImportError:
    from tool import tool
    from compress_json import compress_json
    
# 尽量不使用绝对导入 如from tool import tool
private_server = "https://next.bgm.tv/p1"
public_server = "https://api.bgm.tv/v0"
load_dotenv()

access_token = os.getenv("bangumi_acg_agent_token")
private_headers = {
        # 设置一个规范的用户代理，这是 Bangumi API 的建议，有助于提高请求的成功率和稳定性
        "User-Agent": "mytomori/1.0 (https://github.com/yourusername/your-repo)",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
public_headers = {
        # 设置一个规范的用户代理，这是 Bangumi API 的建议，有助于提高请求的成功率和稳定性
        "User-Agent": "mytomori/1.0 (https://github.com/yourusername/your-repo)",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
comment_keys = {
    "user": {
        "id": None,
    },
    "rate": None,
    "comment": None,

}
staff_keys = {
    "positions": 
        {
            "type": {
                "cn": None,
            }
        },
    "staff": {
        "id": None,
        "nameCN": None,
        "type": 1,
    }
}
# staff_keys = {
#     "positions": None,
#     "staff": {
#         "id": None,
#         "nameCN": None,
#         "type": 1,
#     }
# }
@tool
def fetch_subject_comments(subject_id, limit=10, offset=0):
    url = f"{private_server}/subjects/{subject_id}/comments"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        data = compress_json(data, comment_keys)
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message

@tool
def fetch_character_comment(character_id, limit=5, offset=0):
    url = f"{private_server}/characters/{character_id}/comments"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_episode_info(episode_id):
    url = f"{private_server}/episodes/{episode_id}"
    try:
        resp = requests.get(url, headers=private_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_person_info(person_id):
    url = f"{private_server}/persons/{person_id}"
    try:
        resp = requests.get(url, headers=private_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_collection_subjects(limit=5, offset=0):
    url = f"{private_server}/users/-/collections"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_collection_characters(limit=5, offset=0):
    url = f"{private_server}/users/-/collections/characters"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_collection_indexes(limit=5, offset=0):
    url = f"{private_server}/users/-/collections/indexes"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_relationship(resource_type, resource_id, limit=5, offset=0):
    url = f"{private_server}/{resource_type}/{resource_id}/relations"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


# ==================== Character 相关 ====================
@tool
def fetch_character_info(character_id):
    url = f"{private_server}/characters/{character_id}"
    try:
        resp = requests.get(url, headers=private_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_character_casts(character_id, limit=5, offset=0):
    url = f"{private_server}/characters/{character_id}/casts"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_character_collects(character_id, limit=5, offset=0):
    url = f"{private_server}/characters/{character_id}/collects"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_character_indexes(character_id, limit=5, offset=0):
    url = f"{private_server}/characters/{character_id}/indexes"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_character_relations(character_id, limit=5, offset=0):
    url = f"{private_server}/characters/{character_id}/relations"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


# ==================== Subject 相关 ====================

def fetch_subjects_list(limit=5, offset=0):
    url = f"{private_server}/subjects"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message

@tool
def fetch_subject_info(subject_id):
    url = f"{public_server}/subjects/{subject_id}"
    try:
        resp = requests.get(url, headers=public_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_subject_characters(subject_id, limit=5, offset=0):
    url = f"{private_server}/subjects/{subject_id}/characters"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_subject_collects(subject_id, limit=5, offset=0):
    url = f"{private_server}/subjects/{subject_id}/collects"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_subject_episodes(subject_id, limit=5, offset=0):
    url = f"{private_server}/subjects/{subject_id}/episodes"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_subject_indexes(subject_id, limit=5, offset=0):
    url = f"{private_server}/subjects/{subject_id}/indexes"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_subject_recs(subject_id, limit=5, offset=0):
    url = f"{private_server}/subjects/{subject_id}/recs"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_subject_relations(subject_id, limit=5, offset=0):
    url = f"{private_server}/subjects/{subject_id}/relations"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_subject_reviews(subject_id, limit=5, offset=0):
    url = f"{private_server}/subjects/{subject_id}/reviews"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message

@tool
# 推荐使用此api而非下面的api,因为此api能够高效地进行职位过滤
def fetch_subject_staffs(subject_id, position=[1], limit=5, offset=0):
    """
    获取动画主题的制作人员信息
    :param subject_id: 主题ID
    :param position: 职位编号，可以是整数或列表
                    1-原作 2-导演 3-脚本 4-分镜 5-演出 6-配乐 7-人物原案 8-构图 9-美术监督
                    例如: 1 或 [1,2,3] 或 (1,2)
    :param limit: 每页数量
    :param offset: 偏移量
    """
    url = f"{private_server}/subjects/{subject_id}/staffs/persons"
    
    # 将position转换为列表处理
    positions = [1,2,3]
    all_data = []
    
    try:
        for pos in positions:
            params = {
                "limit": limit,
                "offset": offset,
                "position": pos
            }
            resp = requests.get(url, headers=private_headers, params=params, timeout=5)
            resp.raise_for_status()
            res = resp.json()
            data = res.get("data", [])
            all_data.extend(data)
        data = compress_json(all_data, staff_keys)
        return json.dumps(data, ensure_ascii=False, indent=2)     
    except Exception as e:
        return f"请求失败: {e}"
@tool
def fetch_subject_staff_position(subject_id, limit=5, offset=0):
    url = f"{private_server}/subjects/{subject_id}/staffs/positions"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message

def fetch_subject_topics(subject_id, limit=5, offset=0):
    url = f"{private_server}/subjects/{subject_id}/topics"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


# ==================== Episode 相关 ====================

def fetch_episode_comment(episode_id, limit=5, offset=0):
    url = f"{private_server}/episodes/{episode_id}/comments"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


# ==================== Person 相关 ====================
@tool
def fetch_person_comments(person_id, limit=5, offset=0):
    url = f"{private_server}/persons/{person_id}/comments"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_person_casts(person_id, limit=5, offset=0):
    url = f"{private_server}/persons/{person_id}/casts"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message
        


def fetch_person_collects(person_id, limit=5, offset=0):
    url = f"{private_server}/persons/{person_id}/collects"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_person_indexes(person_id, limit=5, offset=0):
    url = f"{private_server}/persons/{person_id}/indexes"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_person_relations(person_id, limit=5, offset=0):
    url = f"{private_server}/persons/{person_id}/relations"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_person_works(person_id, limit=5, offset=0):
    url = f"{private_server}/persons/{person_id}/works"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


# ==================== Collection 相关 ====================

def fetch_collection_subject_info(subject_id):
    url = f"{private_server}/collections/subjects/{subject_id}"
    try:
        resp = requests.get(url, headers=private_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_collection_character_info(character_id):
    url = f"{private_server}/collections/characters/{character_id}"
    try:
        resp = requests.get(url, headers=private_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_collection_persons(limit=5, offset=0):
    url = f"{private_server}/collections/persons"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_collection_person_info(person_id):
    url = f"{private_server}/collections/persons/{person_id}"
    try:
        resp = requests.get(url, headers=private_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_collection_index_info(index_id):
    url = f"{private_server}/collections/indexes/{index_id}"
    try:
        resp = requests.get(url, headers=private_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_collection_episode_info(episode_id):
    url = f"{private_server}/collections/episodes/{episode_id}"
    try:
        resp = requests.get(url, headers=private_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


# ==================== Index 相关 ====================

def fetch_indexes_list(limit=5, offset=0):
    url = f"{private_server}/indexes"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_index_info(index_id):
    url = f"{private_server}/indexes/{index_id}"
    try:
        resp = requests.get(url, headers=private_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_index_comments(index_id, limit=5, offset=0):
    url = f"{private_server}/indexes/{index_id}/comments"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_index_related(index_id, limit=5, offset=0):
    url = f"{private_server}/indexes/{index_id}/related"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


# ==================== 搜索相关 ====================

def fetch_search_subjects(keywords, limit=5, offset=0):
    url = f"{private_server}/search/subjects"
    params = {
        "keywords": keywords,
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_search_characters(keywords, limit=5, offset=0):
    url = f"{private_server}/search/characters"
    params = {
        "keywords": keywords,
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_search_persons(keywords, limit=5, offset=0):
    url = f"{private_server}/search/persons"
    params = {
        "keywords": keywords,
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


# ==================== 用户相关 ====================

def fetch_user_info(username):
    url = f"{private_server}/users/{username}"
    try:
        resp = requests.get(url, headers=private_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_user_collection_characters(username, limit=5, offset=0):
    url = f"{private_server}/users/{username}/collections/characters"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_user_collection_persons(username, limit=5, offset=0):
    url = f"{private_server}/users/{username}/collections/persons"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_user_collection_indexes(username, limit=5, offset=0):
    url = f"{private_server}/users/{username}/collections/indexes"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_user_blogs(username, limit=5, offset=0):
    url = f"{private_server}/users/{username}/blogs"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message
    return json.dumps(data, ensure_ascii=False, indent=2)


def fetch_current_user_info():
    url = f"{private_server}/me"
    try:
        resp = requests.get(url, headers=private_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_friendlist():
    url = f"{private_server}/friendlist"
    try:
        resp = requests.get(url, headers=private_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_friends(limit=5, offset=0):
    url = f"{private_server}/friends"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


# ==================== 其他相关 ====================

def fetch_calendar():
    url = f"{private_server}/calendar"
    try:
        resp = requests.get(url, headers=private_headers, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message


def fetch_trending_subjects(limit=5, offset=0):
    url = f"{private_server}/trending/subjects"
    params = {
        "limit": limit,
        "offset": offset
    }
    try:
        resp = requests.get(url, headers=private_headers, params=params, timeout=5)
        resp.raise_for_status()
        res = resp.json()
        data = res.get("data", [])
        # 直接打印返回的 JSON 数据（美观输出）
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"请求失败: {e}"
        return error_message
if __name__ == "__main__":
    # res = fetch_subject_info.run({"subject_id": 8})
    # res = fetch_subject_comment.run({"subject_id": 8, "limit": 5, "offset": 0})
    res = fetch_subject_staffs.run({"subject_id": 8, "limit": 5, "offset": 0})
    # res = fetch_person_comments.run({"person_id": 3815, "limit": 2, "offset": 0})
    # res = fetch_subject_comments.run({"subject_id": 8, "limit": 5, "offset": 0})
    print(res)
    print(len(res))