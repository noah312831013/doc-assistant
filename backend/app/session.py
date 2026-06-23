import json

import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

SESSION_EXPIRE_SECONDS = 1800  # 30 分鐘


def set_session(user_id: int, token: str) -> None:
    """登入時儲存 session"""
    key = f"session:{user_id}"
    r.setex(key, SESSION_EXPIRE_SECONDS, json.dumps({"token": token}))


def get_session(user_id: int) -> dict | None:
    """取得 session"""
    key = f"session:{user_id}"
    data = r.get(key)
    return json.loads(data) if data else None


def delete_session(user_id: int) -> None:
    """登出時刪除 session"""
    r.delete(f"session:{user_id}")