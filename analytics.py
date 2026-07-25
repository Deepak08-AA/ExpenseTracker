from database import get_connection


def total_expense(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE user_id = ?
    """, (user_id,))

    total = cursor.fetchone()[0]

    conn.close()

    # If user has no expenses, SUM() returns None
    if total is None:
        return 0

    return total

def max_expense(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT MAX(amount)
        FROM expenses
        WHERE user_id = ?
    """, (user_id,))

    max = cursor.fetchone()[0]
    return max

def min_expense(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT MIN(amount)
        FROM expenses
        WHERE user_id = ?
    """, (user_id,))

    min = cursor.fetchone()[0]
    return min

def expense_by_category(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT category, SUM(amount)
    FROM expenses
    WHERE user_id = ?
    GROUP BY category
    """,(user_id,))

    data = cursor.fetchall()
    conn.close()

    return data


