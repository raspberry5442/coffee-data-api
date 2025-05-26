import sqlite3
import csv


"""
导入订单数据到SQLite数据库
"""

conn = sqlite3.connect('db/coffee.db')
cursor = conn.cursor()

with open('C:/Users/Xuwen Zheng/Downloads/fake_coffee_data2/orders.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # 跳过表头
    for row in reader:
        cursor.execute("INSERT INTO orders (id, timestamp, total_price, customer_id) VALUES (?, ?, ?, ?)", row)

conn.commit()
conn.close()
