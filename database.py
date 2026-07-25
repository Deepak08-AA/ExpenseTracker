import sqlite3
import bcrypt

# ---------------- DATABASE CONNECTION ---------------- #

def get_connection():
    conn = sqlite3.connect("expenseTracker.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- CREATE TABLES ---------------- #

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS USERS(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS EXPENSES(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount INTEGER NOT NULL,
        category TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        date DATE TIME NOT NULL,
        FOREIGN KEY(user_id) REFERENCES USERS(id)
    )
    """)
    conn.commit()
    conn.close()

create_tables()


# ---------------- USER FUNCTIONS ---------------- #

def user_exists(username, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM USERS WHERE username=? OR email=?",
        (username, email)
    )

    user = cursor.fetchone()

    conn.close()
    return user


def create_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    cursor.execute(
        "INSERT INTO USERS(username,email,password) VALUES(?,?,?)",
        (username, email, hashed_password)
    )

    conn.commit()
    conn.close()


def login_user(username, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM USERS WHERE username=? AND email=?",
        (username, email)
    )

    user = cursor.fetchone()

    conn.close()
    return user


def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM USERS WHERE id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()
    return user

# ---------------- EXPENSE FUNCTIONS ---------------- #

def get_records(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM EXPENSES WHERE user_id=?",
        (user_id,)
    )

    records = cursor.fetchall()

    conn.close()
    return records


def add_record(user_id,amount,category,payment_method,date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO EXPENSES(user_id,amount,category,payment_method,date) VALUES (?, ?, ?, ?, ?)",
        (user_id,amount,category,payment_method,date)
    )

    conn.commit()
    conn.close()


def update_record(user_id, id, amount, category, payment_method, date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE EXPENSES SET amount=?, category=?, payment_method=?, date=? WHERE id=? AND user_id=?",
        (amount, category, payment_method, date, id, user_id)
    )

    conn.commit()
    conn.close()


def delete_record(user_id, id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM EXPENSES WHERE id=? AND user_id=?",
        (id,user_id)
    )

    conn.commit()
    conn.close()

def check_record(user_id, id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM EXPENSES WHERE id=? AND user_id=?",
        (id, user_id)
    )

    record = cursor.fetchone()
    conn.close()
    return record

# def get_stats():
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT COUNT(*) FROM users")
#     total = cursor.fetchone()[0]

#     cursor.execute("SELECT COUNT(*) FROM users WHERE difficulty='Easy'")
#     easy = cursor.fetchone()[0]

#     cursor.execute("SELECT COUNT(*) FROM users WHERE difficulty='Medium'")
#     medium = cursor.fetchone()[0]

#     cursor.execute("SELECT COUNT(*) FROM users WHERE difficulty='Hard'")
#     hard = cursor.fetchone()[0]

#     conn.close()
#     return {
#         "total": total,
#         "easy": easy,
#         "medium": medium,
#         "hard": hard
# }