from flask import Blueprint, request, jsonify
import sqlite3
from auth import auth_required


api = Blueprint('api', __name__)
DB_PATH = 'db/coffee.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

@api.route('/coffee_server/get_data', methods=['GET'])
@auth_required
def get_data():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        conn.close()
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

@api.route('/coffee_server/get_meta/', methods=['GET'])
@auth_required
def get_meta():
    conn = get_connection()
    cursor = conn.cursor()

    # 你自定义的注释映射（字段级别）
    column_comments = {
        "customers": {
            "id": "会员ID",
            "name": "会员姓名",
            "membership": "会员等级（NONE=非会员/REGULAR=普通会员/PREMIUM=高级会员）"
        },
        "staff": {
            "id": "员工ID",
            "name": "员工姓名"
        },
        "coffee_types": {
            "id": "咖啡类型ID",
            "name": "咖啡名称",
            "base_price": "基础价格",
            "temp": "温度类型（HOT=热饮/COLD=冷饮）"
        },
        "orders": {
            "id": "订单ID",
            "timestamp": "下单时间",
            "customer_id": "关联的会员ID（可能为空）",
            "source": "订单来源（IN_STORE=进店，ONLINE=线上）",
            "total_price": "订单总金额（已考虑会员折扣）"
        },
        "order_items": {
            "id": "记录ID",
            "order_id": "所属订单ID",
            "coffee_type_id": "咖啡类型ID",
            "staff_id": "制作员工ID",
            "quantity": "咖啡数量",
            "unit_price": "咖啡单价（未考虑折扣）"
        }
    }

    # 数据类型映射（更可读）
    type_map = {
        "TEXT": "VARCHAR",
        "REAL": "FLOAT",
        "INTEGER": "INTEGER",
        "DATETIME": "DATETIME"
    }

    meta_list = []
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']

    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns_info = cursor.fetchall()

        table_meta = {
            "table_name": table,
            "columns": []
        }

        for cid, name, col_type, notnull, default_value, pk in columns_info:
            col_type_upper = col_type.upper()
            readable_type = type_map.get(col_type_upper, col_type_upper)
            column_meta = {
                "name": name,
                "format": readable_type,
                "is_null": not bool(notnull),
                "default": default_value,
                "primary_key": bool(pk),
                "comment": column_comments.get(table, {}).get(name, "")
            }
            table_meta["columns"].append(column_meta)

        meta_list.append(table_meta)

    conn.close()
    return jsonify({"meta": meta_list})

