from flask import request, jsonify
from functools import wraps

# 设置你允许的 API Key（也可以从配置文件读取）
VALID_API_KEYS = {"zxw971202"}

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ")[1]
        if token not in VALID_API_KEYS:
            return jsonify({"error": "Invalid API Key"}), 401

        return f(*args, **kwargs)
    return decorated_function
