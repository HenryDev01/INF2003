import mysql.connector
from pymongo import MongoClient

# Please configure your own db
def get_sql_db():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = 'Project',
        auth_plugin="mysql_native_password"
    )

def get_mongo_db():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Project']
    return db

def get_monthly_order_counts():
    connection = get_sql_db()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS month,
            COUNT(*) AS total_orders
        FROM Orders
        GROUP BY month
        ORDER BY month;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()
    return result

def get_daily_order_counts():
    connection = get_sql_db()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            DATE(order_purchase_timestamp) AS day,
            COUNT(*) AS total_orders
        FROM Orders
        GROUP BY day
        ORDER BY day;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()
    return result

def get_top_products_by_quantity():
    connection = get_sql_db()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT p.product_name, COUNT(*) AS total_quantity
        FROM Order_Items oi
        JOIN product p ON oi.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY total_quantity DESC
        LIMIT 10;
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def get_top_products_by_revenue():
    connection = get_sql_db()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT p.product_name, COUNT(*) * p.price AS total_revenue
        FROM Order_Items oi
        JOIN product p ON oi.product_id = p.product_id
        GROUP BY p.product_name, p.price
        ORDER BY total_revenue DESC
        LIMIT 10;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def get_total_earnings():
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT SUM(price) FROM order_items
    """)
    result = cursor.fetchone()
    db.close()
    return result[0] if result and result[0] else 0

def get_top_geolocation_sales():
    db = None
    cursor = None
    try:
        db = get_sql_db()
        if not db:
            return [], []

        cursor = db.cursor()
        cursor.execute("""
            SELECT
                o.city,
                SUM(oi.price) AS total_revenue
            FROM
                Order_Items oi
            JOIN
                Orders o ON oi.order_id = o.order_id
            GROUP BY
                o.city
            ORDER BY
                total_revenue DESC
            LIMIT 10;
        """)
        results = cursor.fetchall()
        labels = [row[0] for row in results]
        data = [float(row[1]) for row in results]
        return labels, data
    except Exception as e:
        print(f"Error fetching top geolocation sales: {e}")
        return [], []
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def get_top_cat_by_quantity():
    db = None
    cursor = None
    try:
        db = get_sql_db()
        if not db:
            return [], []

        cursor = db.cursor()
        cursor.execute("""
            SELECT
                ct.product_category,
                COUNT(oi.order_id) AS total_quantity
            FROM
                Order_Items oi
            JOIN
                Product p ON oi.product_id = p.product_id
            JOIN
                Category_Translation ct ON p.product_category_translation = ct.product_category_translation
            GROUP BY
                ct.product_category
            ORDER BY
                total_quantity DESC
            LIMIT 10;
        """)
        results = cursor.fetchall()
        labels = [row[0] for row in results]
        data = [int(row[1]) for row in results]
        return labels, data
    except Exception as e:
        print(f"Error fetching top products by quantity: {e}")
        return [], []
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def get_top_cat_by_revenue():
    db = None
    cursor = None
    try:
        db = get_sql_db()
        if not db:
            return [], []

        cursor = db.cursor()
        cursor.execute("""
            SELECT
                ct.product_category,
                SUM(oi.price) AS total_revenue
            FROM
                Order_Items oi
            JOIN
                Product p ON oi.product_id = p.product_id
            JOIN
                Category_Translation ct ON p.product_category_translation = ct.product_category_translation
            GROUP BY
                ct.product_category
            ORDER BY
                total_revenue DESC
            LIMIT 10;
        """)
        results = cursor.fetchall()
        labels = [row[0] for row in results]
        data = [float(row[1]) for row in results]
        return labels, data
    except Exception as e:
        print(f"Error fetching top products by revenue: {e}")
        return [], []
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()