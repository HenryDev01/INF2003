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
def get_to_pack_count(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT COUNT(DISTINCT o.order_id)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE o.order_status = 'Processing' AND p.seller_id = %s;
    """, (seller_id,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result else 0

def get_pending_count(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT COUNT(DISTINCT o.order_id)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE o.order_status = 'Packed' AND p.seller_id = %s;
    """, (seller_id,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result else 0

def get_out_of_stock_count(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM product
        WHERE has_stock = FALSE AND seller_id = %s;
    """, (seller_id,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result else 0

def get_pending_refund_count(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT COUNT(DISTINCT o.order_id)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE o.order_status = 'Refund Requested' AND p.seller_id = %s;
    """, (seller_id,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result else 0

def get_cancellation_and_refund_rates(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT
            SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
            SUM(CASE WHEN o.order_status = 'Refunded' THEN 1 ELSE 0 END) AS refunded_orders,
            COUNT(DISTINCT o.order_id) AS total_orders
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE p.seller_id = %s;
    """, (seller_id,))
    result = cursor.fetchone()
    db.close()

    cancelled = result[0] or 0
    refunded = result[1] or 0
    total = result[2] or 0

    cancellation_rate = (cancelled / total * 100) if total else 0
    refund_rate = (refunded / total * 100) if total else 0

    return cancellation_rate, refund_rate

def get_monthly_average(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT IFNULL(
            SUM(p.price * item_counts.quantity) / NULLIF(COUNT(DISTINCT DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')), 0),
            0
        )
        FROM orders o
        JOIN (
            SELECT order_id, product_id, COUNT(*) AS quantity
            FROM order_items
            GROUP BY order_id, product_id
        ) AS item_counts ON o.order_id = item_counts.order_id
        JOIN product p ON item_counts.product_id = p.product_id
        WHERE p.seller_id = %s;
    """, (seller_id,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result and result[0] else 0

def get_customer_count(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT COUNT(DISTINCT o.customer_id)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE p.seller_id = %s;
    """, (seller_id,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result and result[0] else 0

def get_sales_count(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT COUNT(DISTINCT o.order_id)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE p.seller_id = %s;
    """, (seller_id,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result and result[0] else 0

def get_total_orders_thisMonth(seller_id):
    db = get_sql_db()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT COUNT(DISTINCT o.order_id) AS total_orders_this_month
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE YEAR(o.order_purchase_timestamp) = YEAR(CURDATE())
          AND MONTH(o.order_purchase_timestamp) = MONTH(CURDATE())
          AND p.seller_id = %s;
    """
    cursor.execute(query, (seller_id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result['total_orders_this_month'] if result else 0

def get_total_orders_today(seller_id):
    db = get_sql_db()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT COUNT(DISTINCT o.order_id) AS total_orders_today
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE DATE(o.order_purchase_timestamp) = CURDATE()
          AND p.seller_id = %s;
    """
    cursor.execute(query, (seller_id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result['total_orders_today'] if result else 0

def get_yearly_order(seller_id):
    db = get_sql_db()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT YEAR(o.order_purchase_timestamp) AS order_year,
               COUNT(DISTINCT o.order_id) AS total_orders
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE p.seller_id = %s
        GROUP BY order_year
        ORDER BY order_year;
    """
    cursor.execute(query, (seller_id,))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

def get_thisYear_order(seller_id):
    db = get_sql_db()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT COUNT(DISTINCT o.order_id) AS total_orders_this_year
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE YEAR(o.order_purchase_timestamp) = YEAR(CURDATE())
          AND p.seller_id = %s;
    """
    cursor.execute(query, (seller_id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result['total_orders_this_year'] if result else 0

def get_monthly_order_counts(seller_id):
    db = get_sql_db()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
               COUNT(DISTINCT o.order_id) AS total_orders
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE p.seller_id = %s
        GROUP BY month
        ORDER BY month;
    """
    cursor.execute(query, (seller_id,))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

def get_daily_order_counts(seller_id):
    db = get_sql_db()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT DATE(o.order_purchase_timestamp) AS day,
               COUNT(DISTINCT o.order_id) AS total_orders
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE p.seller_id = %s
        GROUP BY day
        ORDER BY day;
    """
    cursor.execute(query, (seller_id,))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

def get_top_products_by_quantity(seller_id):
    db = get_sql_db()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT p.product_name, COUNT(*) AS total_quantity
        FROM order_items oi
        JOIN product p ON oi.product_id = p.product_id
        WHERE p.seller_id = %s
        GROUP BY p.product_name
        ORDER BY total_quantity DESC
        LIMIT 10;
    """
    cursor.execute(query, (seller_id,))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

def get_top_products_by_revenue(seller_id):
    db = get_sql_db()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT p.product_name, COUNT(*) * p.price AS total_revenue
        FROM order_items oi
        JOIN product p ON oi.product_id = p.product_id
        WHERE p.seller_id = %s
        GROUP BY p.product_name, p.price
        ORDER BY total_revenue DESC
        LIMIT 10;
    """
    cursor.execute(query, (seller_id,))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

def get_total_earnings(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT SUM(p.price)
        FROM order_items oi
        JOIN product p ON oi.product_id = p.product_id
        WHERE p.seller_id = %s;
    """, (seller_id,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result and result[0] else 0

def get_top_geolocation_sales(seller_id):
    db = None
    cursor = None
    try:
        db = get_sql_db()
        if not db:
            return [], []
        cursor = db.cursor()
        cursor.execute("""
            SELECT o.city,
                   SUM(p.price) AS total_revenue
            FROM order_items oi
            JOIN product p ON oi.product_id = p.product_id
            JOIN orders o ON oi.order_id = o.order_id
            WHERE p.seller_id = %s
            GROUP BY o.city
            ORDER BY total_revenue DESC
            LIMIT 10;
        """, (seller_id,))
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

def get_top_cat_by_quantity(seller_id):
    db = None
    cursor = None
    try:
        db = get_sql_db()
        if not db:
            return [], []
        cursor = db.cursor()
        cursor.execute("""
            SELECT ct.product_category,
                   COUNT(oi.order_id) AS total_quantity
            FROM order_items oi
            JOIN product p ON oi.product_id = p.product_id
            JOIN category_translation ct ON p.product_category_translation = ct.product_category_translation
            WHERE p.seller_id = %s
            GROUP BY ct.product_category
            ORDER BY total_quantity DESC
            LIMIT 10;
        """, (seller_id,))
        results = cursor.fetchall()
        labels = [row[0] for row in results]
        data = [int(row[1]) for row in results]
        return labels, data
    except Exception as e:
        print(f"Error fetching top categories by quantity: {e}")
        return [], []
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def get_top_cat_by_revenue(seller_id):
    db = None
    cursor = None
    try:
        db = get_sql_db()
        if not db:
            return [], []
        cursor = db.cursor()
        cursor.execute("""
            SELECT ct.product_category_translation,
                   SUM(p.price) AS total_revenue
            FROM order_items oi
            JOIN product p ON oi.product_id = p.product_id
            JOIN category_translation ct ON p.product_category_translation = ct.product_category_translation
            WHERE p.seller_id = %s
            GROUP BY ct.product_category_translation
            ORDER BY total_revenue DESC
            LIMIT 10;
        """, (seller_id,))
        results = cursor.fetchall()
        labels = [row[0] for row in results]
        data = [float(row[1]) for row in results]
        return labels, data
    except Exception as e:
        print(f"Error fetching top categories by revenue: {e}")
        return [], []
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def get_revenue_today(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT SUM(p.price)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE DATE(o.order_purchase_timestamp) = CURDATE()
          AND p.seller_id = %s;
    """, (seller_id,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result and result[0] else 0

def get_revenue_this_month(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT SUM(p.price)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE YEAR(o.order_purchase_timestamp) = YEAR(CURDATE())
          AND MONTH(o.order_purchase_timestamp) = MONTH(CURDATE())
          AND p.seller_id = %s;
    """, (seller_id,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result and result[0] else 0

def get_revenue_this_year(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT SUM(p.price)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE YEAR(o.order_purchase_timestamp) = YEAR(CURDATE())
          AND p.seller_id = %s;
    """, (seller_id,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result and result[0] else 0

def get_daily_revenue(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT DATE(o.order_purchase_timestamp), SUM(p.price)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE p.seller_id = %s
        GROUP BY DATE(o.order_purchase_timestamp)
        ORDER BY DATE(o.order_purchase_timestamp);
    """, (seller_id,))
    results = cursor.fetchall()
    db.close()
    return [
        {
            "date": str(row[0]),
            "revenue": float(row[1]) if row[1] else 0
        }
        for row in results
    ]

def get_monthly_revenue(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS order_month,
               SUM(p.price)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE p.seller_id = %s
        GROUP BY order_month
        ORDER BY order_month;
    """, (seller_id,))
    results = cursor.fetchall()
    db.close()
    return [
        {
            "month": row[0],
            "revenue": float(row[1]) if row[1] else 0
        }
        for row in results
    ]

def get_yearly_revenue(seller_id):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT YEAR(o.order_purchase_timestamp) AS order_year,
               SUM(p.price)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN product p ON oi.product_id = p.product_id
        WHERE p.seller_id = %s
        GROUP BY order_year
        ORDER BY order_year;
    """, (seller_id,))
    results = cursor.fetchall()
    db.close()
    return [
        {
            "year": str(row[0]),
            "revenue": float(row[1]) if row[1] else 0
        }
        for row in results
    ]
