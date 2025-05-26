import sqlite3

def init_db():
    conn = sqlite3.connect('db/coffee.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        membership TEXT CHECK(membership IN ('ONE', 'REGULAR', 'PREMIUM'))
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS coffee_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        base_price REAL,
        temp TEXT CHECK(temp IN ('HOT', 'COLD'))
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        customer_id INTEGER,
        source TEXT CHECK(source IN ('IN_STORE', 'ONLINE')),
        total_price REAL,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        coffee_type_id INTEGER,
        staff_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(coffee_type_id) REFERENCES coffee_types(id),
        FOREIGN KEY(staff_id) REFERENCES staff(id)
    )
    ''')

    conn.commit()
    conn.close()
