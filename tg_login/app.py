from flask import Flask, request, jsonify
import hashlib
import hmac
import uuid
import sqlite3
import time
import os

app = Flask(__name__)
app.config['TELEGRAM_BOT_TOKEN'] = os.getenv('TELEGRAM_BOT_TOKEN', '')

DB_PATH = os.path.join("..", "plana", "myplana.sqlite")

# ===========================
# Работа с базой данных
# ===========================
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Создание таблиц при старте
with get_db_connection() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            photo_url TEXT,
            created INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT,
            token TEXT,
            created INTEGER,
            authorized INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            title TEXT,
            description TEXT,
            start_date TEXT,
            start_time TEXT,
            end_date TEXT,
            end_time TEXT,
            created INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,          -- число (например 5)
            unit TEXT NOT NULL,               -- 'минут', 'часов', 'дней', 'месяцев', 'лет'
            via_tg INTEGER DEFAULT 0,         -- 0/1 (отправлять ли в Telegram)
            created INTEGER,

            FOREIGN KEY(task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
        )
    """)
    conn.commit()

# ===========================
# Проверка HMAC от Telegram
# ===========================
def check_telegram_hash(data: dict) -> bool:
    data_copy = data.copy()
    hash_received = data_copy.pop('hash', None)
    data_list = [f"{k}={v}" for k, v in sorted(data_copy.items()) if v is not None]
    data_string = '\n'.join(data_list).encode('utf-8')
    secret_key = hashlib.sha256(app.config['TELEGRAM_BOT_TOKEN'].encode('utf-8')).digest()
    hmac_check = hmac.new(secret_key, data_string, hashlib.sha256).hexdigest()
    return hmac_check == hash_received

# ===========================
# Маршруты
# ===========================
@app.route('/')
def index():
    session_id = request.args.get("session_id", "")
    return f"""
    <body>
        <script async
            src="https://telegram.org/js/telegram-widget.js?16"
            data-telegram-login="AiCurseBot"
            data-size="large"
            data-auth-url="https://fitfully-delectable-ray.cloudpub.ru/login/telegram?session_id={session_id}"
            data-request-access="write">
        </script>
    </body>
    """

# ===========================
# Получение всех уведомлений
# ===========================
@app.route("/all_notifications")
def all_notifications():
    with get_db_connection() as conn:
        notifications = conn.execute("SELECT * FROM notifications").fetchall()
        result = [dict(n) for n in notifications]
    return jsonify(result)

# ===========================
# Получение всех задач
# ===========================
@app.route("/all_tasks")
def all_tasks():
    with get_db_connection() as conn:
        tasks = conn.execute("SELECT * FROM tasks").fetchall()
        result = [dict(t) for t in tasks]
    return jsonify(result)

# ===========================
# Получение всех пользователей (для бота)
# ===========================
@app.route("/users_with_sessions")
def users_with_sessions():
    with get_db_connection() as conn:
        users = conn.execute("SELECT user_id FROM users").fetchall()
        # Просто возвращаем всех пользователей, у которых есть user_id
        result = [u["user_id"] for u in users if u["user_id"]]
    return jsonify(result)


@app.route("/register_session")
def register_session():
    session_id = str(uuid.uuid4())
    created = int(time.time())
    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO sessions (session_id, created, authorized) VALUES (?, ?, ?)",
            (session_id, created, 0)
        )
        conn.commit()
    return jsonify({"session_id": session_id})

@app.route("/session_status/<session_id>")
def session_status(session_id):
    with get_db_connection() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,)).fetchone()
    if not session or not session["authorized"]:
        return jsonify({"authorized": False, "user": None})

    user = None
    with get_db_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE user_id = ?", (session["user_id"],)).fetchone()

    user_data = {
        "user_id": user["user_id"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "username": user["username"],
        "photo_url": user["photo_url"]
    }

    return jsonify({"authorized": True, "user": user_data})

@app.route('/login/telegram')
def login_telegram():
    session_id = request.args.get("session_id")
    if not session_id:
        return "Session ID is required", 400

    with get_db_connection() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,)).fetchone()
    if not session:
        return "Unknown session", 400

    data = {
        'id': request.args.get('id'),
        'first_name': request.args.get('first_name'),
        'last_name': request.args.get('last_name'),
        'username': request.args.get('username'),
        'photo_url': request.args.get('photo_url'),
        'auth_date': request.args.get('auth_date'),
        'hash': request.args.get('hash')
    }

    if not check_telegram_hash(data):
        return 'Authorization failed', 403

    user_id = data['id']
    token = hashlib.sha256(f"{user_id}{data['auth_date']}".encode()).hexdigest()
    created = int(time.time())

    with get_db_connection() as conn:
        existing_user = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if not existing_user:
            conn.execute("""
                INSERT INTO users (user_id, first_name, last_name, username, photo_url, created)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, data['first_name'], data['last_name'], data['username'], data['photo_url'], created))

        existing_session = conn.execute("SELECT * FROM sessions WHERE user_id = ?", (user_id,)).fetchone()
        if existing_session:
            conn.execute("DELETE FROM sessions WHERE session_id=?", (existing_session['session_id'],))

        conn.execute("""
            UPDATE sessions
            SET user_id=?, token=?, authorized=?, created=?
            WHERE session_id=?
        """, (user_id, token, 1, created, session_id))
        conn.commit()

    print("Telegram user authorized:", data)
    return f"{user_id} is Authorized! You can close this window.\nSession: {session_id}"

@app.route("/logout", methods=["POST"])
def logout():
    session_id = request.json.get("session_id")
    if not session_id:
        return jsonify({"error": "Session ID required"}), 400

    with get_db_connection() as conn:
        conn.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))
        conn.commit()
    return jsonify({"message": "Logged out successfully"})

# ===========================
# Работа с задачами
# ===========================
@app.route("/tasks", methods=["GET"])
def get_tasks():
    session_id = request.args.get("session_id")
    with get_db_connection() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        if not session or not session["authorized"]:
            return jsonify({"error": "Unauthorized"}), 403
        tasks = conn.execute("SELECT * FROM tasks WHERE user_id=?", (session["user_id"],)).fetchall()
    return jsonify([dict(task) for task in tasks])

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    session_id = data.get("session_id")
    with get_db_connection() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        if not session or not session["authorized"]:
            return jsonify({"error": "Unauthorized"}), 403
        created = int(time.time())
        conn.execute("""
            INSERT INTO tasks (user_id, title, description, start_date, start_time, end_date, end_time, created)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session["user_id"], data.get("title"), data.get("description"),
            data.get("start_date"), data.get("start_time"),
            data.get("end_date"), data.get("end_time"), created
        ))
        conn.commit()
    return jsonify({"message": "Task created"})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    session_id = request.args.get("session_id")
    with get_db_connection() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        if not session or not session["authorized"]:
            return jsonify({"error": "Unauthorized"}), 403
        conn.execute("DELETE FROM tasks WHERE task_id=? AND user_id=?", (task_id, session["user_id"]))
        conn.commit()
    return jsonify({"message": "Task deleted"})

# ===========================
# Работа с уведомлениями
# ===========================

@app.route("/tasks/<int:task_id>/notifications", methods=["GET"])
def get_notifications(task_id):
    session_id = request.args.get("session_id")
    with get_db_connection() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        if not session or not session["authorized"]:
            return jsonify({"error": "Unauthorized"}), 403

        # Проверим, что задача принадлежит юзеру
        task = conn.execute("SELECT * FROM tasks WHERE task_id=? AND user_id=?", (task_id, session["user_id"])).fetchone()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        notifications = conn.execute("SELECT * FROM notifications WHERE task_id=?", (task_id,)).fetchall()
    return jsonify([dict(row) for row in notifications])


@app.route("/tasks/<int:task_id>/notifications", methods=["POST"])
def add_notifications(task_id):
    data = request.json
    session_id = data.get("session_id")
    notifications = data.get("notifications", [])  # список [{amount, unit, via_tg}, ...]

    with get_db_connection() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        if not session or not session["authorized"]:
            return jsonify({"error": "Unauthorized"}), 403

        # проверка, что задача принадлежит пользователю
        task = conn.execute("SELECT * FROM tasks WHERE task_id=? AND user_id=?", (task_id, session["user_id"])).fetchone()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        created = int(time.time())
        for n in notifications:
            conn.execute("""
                INSERT INTO notifications (task_id, amount, unit, via_tg, created)
                VALUES (?, ?, ?, ?, ?)
            """, (
                task_id, n.get("amount"), n.get("unit"), int(n.get("via_tg", 0)), created
            ))
        conn.commit()
    return jsonify({"message": "Notifications added"})

@app.route("/tasks/<int:task_id>/notifications/<int:notification_id>", methods=["DELETE"])
def delete_notification(task_id, notification_id):
    session_id = request.args.get("session_id")
    with get_db_connection() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        if not session or not session["authorized"]:
            return jsonify({"error": "Unauthorized"}), 403

        # проверка принадлежности
        task = conn.execute("SELECT * FROM tasks WHERE task_id=? AND user_id=?", (task_id, session["user_id"])).fetchone()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        conn.execute("DELETE FROM notifications WHERE id=? AND task_id=?", (notification_id, task_id))
        conn.commit()
    return jsonify({"message": "Notification deleted"})

@app.route("/tasks/<int:task_id>/notifications", methods=["PUT"])
def update_all_notifications(task_id):
    data = request.json
    session_id = data.get("session_id")
    notifications = data.get("notifications", [])

    with get_db_connection() as conn:
        # проверка сессии
        session = conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        if not session or not session["authorized"]:
            return jsonify({"error": "Unauthorized"}), 403

        # проверка принадлежности задачи
        task = conn.execute("SELECT * FROM tasks WHERE task_id=? AND user_id=?", 
                            (task_id, session["user_id"])).fetchone()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        # удаляем старые уведомления
        conn.execute("DELETE FROM notifications WHERE task_id=?", (task_id,))

        # вставляем новые
        for n in notifications:
            conn.execute("""
                INSERT INTO notifications (task_id, amount, unit, via_tg)
                VALUES (?, ?, ?, ?)
            """, (task_id, n["amount"], n["unit"], int(n.get("via_tg", 0))))

        conn.commit()
    return jsonify({"message": "Notifications updated"})



@app.route("/tasks/<int:task_id>/notifications/<int:notification_id>", methods=["PUT"])
def update_notification(task_id, notification_id):
    data = request.json
    session_id = data.get("session_id")

    with get_db_connection() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        if not session or not session["authorized"]:
            return jsonify({"error": "Unauthorized"}), 403

        task = conn.execute("SELECT * FROM tasks WHERE task_id=? AND user_id=?", (task_id, session["user_id"])).fetchone()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        # Сначала проверяем, есть ли уведомление с таким id
        existing = conn.execute("SELECT * FROM notifications WHERE id=? AND task_id=?", (notification_id, task_id)).fetchone()
        if existing:
            # Обновляем
            conn.execute("""
                UPDATE notifications
                SET amount=?, unit=?, via_tg=?
                WHERE id=? AND task_id=?
            """, (
                data.get("amount"), data.get("unit"), int(data.get("via_tg", 0)),
                notification_id, task_id
            ))
        else:
            # Если нет — создаём новое
            created = int(time.time())
            conn.execute("""
                INSERT INTO notifications (task_id, amount, unit, via_tg, created)
                VALUES (?, ?, ?, ?, ?)
            """, (
                task_id, data.get("amount"), data.get("unit"), int(data.get("via_tg", 0)), created
            ))
        conn.commit()

    return jsonify({"message": "Notification updated or created"})


# ===========================
# Запуск сервера
# ===========================
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)


# from flask import Flask, request, jsonify
# import hashlib
# import hmac
# import uuid
# import sqlite3
# import time
# import os

# app = Flask(__name__)
# app.config['TELEGRAM_BOT_TOKEN'] = os.getenv('TELEGRAM_BOT_TOKEN', '')

# # Путь к базе данных SQLite
# DB_PATH = os.path.join("..", "plana", "myplana.sqlite")

# # ===========================
# # Работа с базой данных
# # ===========================
# def get_db_connection():
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn

# # Создание таблиц при старте сервера
# with get_db_connection() as conn:
#     conn.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             user_id TEXT PRIMARY KEY,
#             first_name TEXT,
#             last_name TEXT,
#             username TEXT,
#             photo_url TEXT,
#             created INTEGER
#         )
#     """)
#     conn.execute("""
#         CREATE TABLE IF NOT EXISTS sessions (
#             session_id TEXT PRIMARY KEY,
#             user_id TEXT,
#             token TEXT,
#             created INTEGER,
#             authorized INTEGER DEFAULT 0
#         )
#     """)
#     conn.commit()

# # ===========================
# # Проверка HMAC от Telegram
# # ===========================
# def check_telegram_hash(data: dict) -> bool:
#     """Проверяет корректность подписи Telegram"""
#     data_copy = data.copy()
#     hash_received = data_copy.pop('hash', None)

#     data_list = [f"{k}={v}" for k, v in sorted(data_copy.items()) if v is not None]
#     data_string = '\n'.join(data_list).encode('utf-8')

#     secret_key = hashlib.sha256(app.config['TELEGRAM_BOT_TOKEN'].encode('utf-8')).digest()
#     hmac_check = hmac.new(secret_key, data_string, hashlib.sha256).hexdigest()
#     return hmac_check == hash_received

# # ===========================
# # Маршруты
# # ===========================
# @app.route('/')
# def index():
#     session_id = request.args.get("session_id", "")
#     return f"""
#     <body>
#         <script async
#             src="https://telegram.org/js/telegram-widget.js?16"
#             data-telegram-login="AiCurseBot"
#             data-size="large"
#             data-auth-url="https://fitfully-delectable-ray.cloudpub.ru/login/telegram?session_id={session_id}"
#             data-request-access="write">
#         </script>
#     </body>
#     """

# @app.route("/register_session")
# def register_session():
#     session_id = str(uuid.uuid4())
#     created = int(time.time())
#     with get_db_connection() as conn:
#         conn.execute(
#             "INSERT INTO sessions (session_id, created, authorized) VALUES (?, ?, ?)",
#             (session_id, created, 0)
#         )
#         conn.commit()
#     return jsonify({"session_id": session_id})

# @app.route("/session_status/<session_id>")
# def session_status(session_id):
#     with get_db_connection() as conn:
#         session = conn.execute(
#             "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
#         ).fetchone()

#     if not session or not session["authorized"]:
#         return jsonify({"authorized": False, "user": None})

#     with get_db_connection() as conn:
#         user = conn.execute(
#             "SELECT * FROM users WHERE user_id = ?", (session["user_id"],)
#         ).fetchone()

#     user_data = {
#         "user_id": user["user_id"],
#         "first_name": user["first_name"],
#         "last_name": user["last_name"],
#         "username": user["username"],
#         "photo_url": user["photo_url"]
#     }

#     return jsonify({"authorized": True, "user": user_data})

# @app.route('/login/telegram')
# def login_telegram():
#     session_id = request.args.get("session_id")
#     if not session_id:
#         return "Session ID is required", 400

#     with get_db_connection() as conn:
#         session = conn.execute(
#             "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
#         ).fetchone()
#     if not session:
#         return "Unknown session", 400

#     data = {
#         'id': request.args.get('id'),
#         'first_name': request.args.get('first_name'),
#         'last_name': request.args.get('last_name'),
#         'username': request.args.get('username'),
#         'photo_url': request.args.get('photo_url'),
#         'auth_date': request.args.get('auth_date'),
#         'hash': request.args.get('hash')
#     }

#     if not check_telegram_hash(data):
#         return 'Authorization failed', 403

#     user_id = data['id']
#     token = hashlib.sha256(f"{user_id}{data['auth_date']}".encode()).hexdigest()
#     created = int(time.time())

#     with get_db_connection() as conn:
#         # Добавляем пользователя в users, если его нет
#         existing_user = conn.execute(
#             "SELECT * FROM users WHERE user_id = ?", (user_id,)
#         ).fetchone()
#         if not existing_user:
#             conn.execute("""
#                 INSERT INTO users (user_id, first_name, last_name, username, photo_url, created)
#                 VALUES (?, ?, ?, ?, ?, ?)
#             """, (user_id, data['first_name'], data['last_name'], data['username'], data['photo_url'], created))

#         # Удаляем старую сессию пользователя, если есть
#         existing_session = conn.execute(
#             "SELECT * FROM sessions WHERE user_id = ?", (user_id,)
#         ).fetchone()
#         if existing_session:
#             conn.execute("DELETE FROM sessions WHERE session_id=?", (existing_session['session_id'],))

#         # Обновляем текущую сессию
#         conn.execute("""
#             UPDATE sessions
#             SET user_id=?, token=?, authorized=?, created=?
#             WHERE session_id=?
#         """, (user_id, token, 1, created, session_id))
#         conn.commit()

#     print("Telegram user authorized:", data)
#     return f"{user_id} is Authorized! You can close this window.\nSession: {session_id}"

# @app.route("/logout", methods=["POST"])
# def logout():
#     session_id = request.json.get("session_id")
#     if not session_id:
#         return jsonify({"error": "Session ID required"}), 400

#     with get_db_connection() as conn:
#         conn.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))
#         conn.commit()
#     return jsonify({"message": "Logged out successfully"})

# # ===========================
# # Запуск сервера
# # ===========================
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8000, debug=True)




# from flask import Flask, request, jsonify
# import hashlib
# import hmac
# import uuid
# import sqlite3
# import time
# import os

# app = Flask(__name__)
# app.config['TELEGRAM_BOT_TOKEN'] = os.getenv('TELEGRAM_BOT_TOKEN', '')

# # Путь к базе данных SQLite
# DB_PATH = os.path.join("..", "plana", "myplana.sqlite")

# # ===========================
# # Работа с базой данных
# # ===========================
# def get_db_connection():
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn

# # Создание таблицы сессий при старте сервера
# with get_db_connection() as conn:
#     conn.execute("""
#         CREATE TABLE IF NOT EXISTS sessions (
#             session_id TEXT PRIMARY KEY,
#             user_id TEXT,
#             token TEXT,
#             created INTEGER,
#             authorized INTEGER DEFAULT 0,
#             first_name TEXT,
#             last_name TEXT,
#             username TEXT,
#             photo_url TEXT
#         )
#     """)
#     conn.commit()

# # ===========================
# # Проверка HMAC от Telegram
# # ===========================
# def check_telegram_hash(data: dict) -> bool:
#     """Проверяет корректность подписи Telegram"""
#     data_copy = data.copy()
#     hash_received = data_copy.pop('hash', None)

#     data_list = [f"{k}={v}" for k, v in sorted(data_copy.items()) if v is not None]
#     data_string = '\n'.join(data_list).encode('utf-8')

#     secret_key = hashlib.sha256(app.config['TELEGRAM_BOT_TOKEN'].encode('utf-8')).digest()
#     hmac_check = hmac.new(secret_key, data_string, hashlib.sha256).hexdigest()
#     return hmac_check == hash_received

# # ===========================
# # Маршруты
# # ===========================
# @app.route('/')
# def index():
#     """Главная страница с Telegram Login виджетом"""
#     session_id = request.args.get("session_id", "")
#     return f"""
#     <body>
#         <script async
#             src="https://telegram.org/js/telegram-widget.js?16"
#             data-telegram-login="AiCurseBot"
#             data-size="large"
#             data-auth-url="https://fitfully-delectable-ray.cloudpub.ru/login/telegram?session_id={session_id}"
#             data-request-access="write">
#         </script>
#     </body>
#     """

# @app.route("/register_session")
# def register_session():
#     """Создание новой сессии"""
#     session_id = str(uuid.uuid4())
#     created = int(time.time())
#     with get_db_connection() as conn:
#         conn.execute(
#             "INSERT INTO sessions (session_id, created, authorized) VALUES (?, ?, ?)",
#             (session_id, created, 0)
#         )
#         conn.commit()
#     return jsonify({"session_id": session_id})

# @app.route("/session_status/<session_id>")
# def session_status(session_id):
#     """Проверка статуса сессии"""
#     with get_db_connection() as conn:
#         row = conn.execute(
#             "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
#         ).fetchone()

#     if not row:
#         return jsonify({"authorized": False, "user": None})

#     user_data = None
#     if row["authorized"]:
#         user_data = {
#             "user_id": row["user_id"],
#             "first_name": row["first_name"] if "first_name" in row.keys() else "Unknown",
#             "last_name": row["last_name"] if "last_name" in row.keys() else None,
#             "username": row["username"] if "username" in row.keys() else None,
#             "photo_url": row["photo_url"] if "photo_url" in row.keys() else None
#         }

#     return jsonify({
#         "authorized": bool(row["authorized"]),
#         "user": user_data
#     })

# @app.route('/login/telegram')
# def login_telegram():
#     """Обработка авторизации через Telegram"""
#     session_id = request.args.get("session_id")
#     if not session_id:
#         return "Session ID is required", 400

#     with get_db_connection() as conn:
#         row = conn.execute(
#             "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
#         ).fetchone()
#     if not row:
#         return "Unknown session", 400

#     data = {
#         'id': request.args.get('id'),
#         'first_name': request.args.get('first_name'),
#         'last_name': request.args.get('last_name'),
#         'username': request.args.get('username'),
#         'photo_url': request.args.get('photo_url'),
#         'auth_date': request.args.get('auth_date'),
#         'hash': request.args.get('hash')
#     }

#     if not check_telegram_hash(data):
#         return 'Authorization failed', 403

#     user_id = data['id']
#     token = hashlib.sha256(f"{user_id}{data['auth_date']}".encode()).hexdigest()
#     created = int(time.time())

#     with get_db_connection() as conn:
#         # удаляем старую сессию пользователя, если есть
#         existing = conn.execute("SELECT * FROM sessions WHERE user_id = ?", (user_id,)).fetchone()
#         if existing:
#             conn.execute("DELETE FROM sessions WHERE session_id=?", (existing['session_id'],))

#         # обновляем текущую сессию
#         conn.execute("""
#             UPDATE sessions
#             SET user_id=?, token=?, authorized=?, created=?,
#                 first_name=?, last_name=?, username=?, photo_url=?
#             WHERE session_id=?
#         """, (
#             user_id, token, 1, created,
#             data['first_name'], data['last_name'], data['username'], data['photo_url'],
#             session_id
#         ))
#         conn.commit()

#     print("Telegram user authorized:", data)
#     return f"{user_id} is Authorized! You can close this window.\nSession: {session_id}"

# @app.route("/logout", methods=["POST"])
# def logout():
#     """Выход пользователя и удаление сессии"""
#     session_id = request.json.get("session_id")
#     if not session_id:
#         return jsonify({"error": "Session ID required"}), 400

#     with get_db_connection() as conn:
#         conn.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))
#         conn.commit()
#     return jsonify({"message": "Logged out successfully"})

# # ===========================
# # Запуск сервера
# # ===========================
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8000, debug=True)


# # from flask import Flask, request, jsonify
# # import hashlib
# # import hmac
# # import uuid
# # import sqlite3
# # import time
# # import os

# # app = Flask(__name__)
# # app.config['TELEGRAM_BOT_TOKEN'] = os.getenv('TELEGRAM_BOT_TOKEN', '')

# # # Путь к базе данных SQLite
# # DB_PATH = os.path.join("..", "plana", "myplana.sqlite")

# # # ===========================
# # # Работа с базой данных
# # # ===========================
# # def get_db_connection():
# #     conn = sqlite3.connect(DB_PATH)
# #     conn.row_factory = sqlite3.Row
# #     return conn

# # # Создаем таблицу сессий при старте сервера
# # with get_db_connection() as conn:
# #     conn.execute("""
# #         CREATE TABLE IF NOT EXISTS sessions (
# #             session_id TEXT PRIMARY KEY,
# #             user_id TEXT,
# #             token TEXT,
# #             created INTEGER,
# #             authorized INTEGER DEFAULT 0
# #         )
# #     """)
# #     conn.commit()

# # # ===========================
# # # Проверка HMAC от Telegram
# # # ===========================
# # def check_telegram_hash(data: dict) -> bool:
# #     """Проверяет корректность подписи Telegram"""
# #     data_copy = data.copy()
# #     hash_received = data_copy.pop('hash', None)

# #     data_list = [f"{k}={v}" for k, v in sorted(data_copy.items()) if v is not None]
# #     data_string = '\n'.join(data_list).encode('utf-8')

# #     secret_key = hashlib.sha256(app.config['TELEGRAM_BOT_TOKEN'].encode('utf-8')).digest()
# #     hmac_check = hmac.new(secret_key, data_string, hashlib.sha256).hexdigest()
# #     return hmac_check == hash_received

# # # ===========================
# # # Маршруты
# # # ===========================
# # @app.route('/')
# # def index():
# #     """Главная страница с Telegram Login виджетом"""
# #     session_id = request.args.get("session_id", "")
# #     return f"""
# #     <body>
# #         <script async
# #             src="https://telegram.org/js/telegram-widget.js?16"
# #             data-telegram-login="AiCurseBot"
# #             data-size="large"
# #             data-auth-url="https://fitfully-delectable-ray.cloudpub.ru/login/telegram?session_id={session_id}"
# #             data-request-access="write">
# #         </script>
# #     </body>
# #     """

# # @app.route("/register_session")
# # def register_session():
# #     """Создание новой сессии"""
# #     session_id = str(uuid.uuid4())
# #     created = int(time.time())
# #     with get_db_connection() as conn:
# #         conn.execute(
# #             "INSERT INTO sessions (session_id, created, authorized) VALUES (?, ?, ?)",
# #             (session_id, created, 0)
# #         )
# #         conn.commit()
# #     return jsonify({"session_id": session_id})

# # @app.route("/session_status/<session_id>")
# # def session_status(session_id):
# #     with get_db_connection() as conn:
# #         row = conn.execute(
# #             "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
# #         ).fetchone()

# #     if row:
# #         user_data = None
# #         if row["authorized"]:
# #             user_data = {
# #                 "user_id": row["user_id"],
# #                 "first_name": row.get("first_name") or "Unknown",
# #                 "last_name": row.get("last_name"),
# #                 "username": row.get("username"),
# #                 "photo_url": row.get("photo_url")
# #             }

# #         return jsonify({
# #             "authorized": bool(row["authorized"]),
# #             "user": user_data
# #         })

# #     return jsonify({"authorized": False, "user": None})
# # # @app.route("/session_status/<session_id>")
# # # def session_status(session_id):
# # #     """Проверка статуса сессии"""
# # #     with get_db_connection() as conn:
# # #         row = conn.execute(
# # #             "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
# # #         ).fetchone()
# # #     if row:
# # #         return jsonify({
# # #             "authorized": bool(row["authorized"]),
# # #             "user": dict(row) if row["authorized"] else None
# # #         })
# # #     return jsonify({"authorized": False})

# # @app.route('/login/telegram')
# # def login_telegram():
# #     """Обработка авторизации через Telegram"""
# #     session_id = request.args.get("session_id")
# #     if not session_id:
# #         return "Session ID is required", 400

# #     with get_db_connection() as conn:
# #         row = conn.execute(
# #             "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
# #         ).fetchone()
# #     if not row:
# #         return "Unknown session", 400

# #     # Получаем данные от Telegram
# #     data = {
# #         'id': request.args.get('id'),
# #         'first_name': request.args.get('first_name'),
# #         'last_name': request.args.get('last_name'),
# #         'username': request.args.get('username'),
# #         'photo_url': request.args.get('photo_url'),
# #         'auth_date': request.args.get('auth_date'),
# #         'hash': request.args.get('hash')
# #     }

# #     if not check_telegram_hash(data):
# #         return 'Authorization failed', 403

# #     # Генерация токена
# #     user_id = data['id']
# #     token = hashlib.sha256(f"{data['id']}{data['auth_date']}".encode()).hexdigest()
# #     created = int(time.time())

# #     with get_db_connection() as conn:
# #         # Проверка существующей сессии пользователя
# #         existing = conn.execute(
# #         "SELECT * FROM sessions WHERE user_id = ?", (user_id,)
# #         ).fetchone()
# #         if existing:
# #             # старую сессию удаляем
# #             conn.execute("DELETE FROM sessions WHERE session_id=?", (existing['session_id'],))
# #         # existing = conn.execute(
# #         #     "SELECT * FROM sessions WHERE user_id = ?", (user_id,)
# #         # ).fetchone()
# #         # if existing:
# #         #     return f"User {user_id} already has an active session ({existing['session_id']})", 403

# #         # Обновляем текущую сессию с данными пользователя
# #         conn.execute("""
# #             UPDATE sessions
# #             SET user_id=?, token=?, authorized=?, created=?,
# #                 first_name=?, last_name=?, username=?, photo_url=?
# #             WHERE session_id=?
# #         """, (
# #             user_id, token, 1, created,
# #             data['first_name'], data['last_name'], data['username'], data['photo_url'],
# #             session_id
# #         ))
# #         conn.commit()

# #     print("Telegram user authorized:", data)
# #     return f"{user_id} is Authorized! You can close this window.\nSession: {session_id}"

# # @app.route("/logout", methods=["POST"])
# # def logout():
# #     """Выход пользователя и удаление сессии"""
# #     session_id = request.json.get("session_id")
# #     if not session_id:
# #         return jsonify({"error": "Session ID required"}), 400

# #     with get_db_connection() as conn:
# #         conn.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))
# #         conn.commit()
# #     return jsonify({"message": "Logged out successfully"})

# # # ===========================
# # # Запуск сервера
# # # ===========================
# # if __name__ == "__main__":
# #     app.run(host='0.0.0.0', port=8000, debug=True)


# # # from flask import Flask, request, jsonify
# # # import secrets
# # # import hmac
# # # import json
# # # import uuid
# # # import hashlib
# # # import sqlite3
# # # import time
# # # # import sys
# # # from os import getenv
# # # import os
# # # # import sys
# # # # import ../plana/mainwi
# # # # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# # # # sys.path.append(path.abspath(path.join(path.dirname(__file__), '../plana')))
# # # # from plana.mainwindow import MainWindow
# # # # from mainwindow import MainWindows

# # # app = Flask(__name__)
# # # app.config['TELEGRAM_BOT_TOKEN'] = getenv('TELEGRAM_BOT_TOKEN')

# # # DB_PATH = os.path.join("..", "plana", "myplana.sqlite")
# # # print(DB_PATH)

# # # sessions = {}
# # # user_sessions = {} # user_id -> session_id


# # # # print(MainWindow.is_authorized)

# # # def get_db_connection():
# # #     conn = sqlite3.connect(DB_PATH)
# # #     conn.row_factory = sqlite3.Row
# # #     return conn

# # # # Создаем таблицу сессий при старте сервера
# # # with get_db_connection() as conn:
# # #     conn.execute("""
# # #         CREATE TABLE IF NOT EXISTS sessions (
# # #             session_id TEXT PRIMARY KEY,
# # #             user_id TEXT,
# # #             token TEXT,
# # #             created INTEGER,
# # #             authorized INTEGER DEFAULT 0
# # #         )
# # #     """)
# # #     conn.commit()


# # # @app.route('/')
# # # def index():
# # #     session_id = request.args.get("session_id")
# # #     return f'''
# # #     <body>
# # #         <script async 
# # #             src="https://telegram.org/js/telegram-widget.js?16" 
# # #             data-telegram-login="AiCurseBot" 
# # #             data-size="large" 
# # #             data-auth-url="https://fitfully-delectable-ray.cloudpub.ru/login/telegram?session_id={session_id}" 
# # #             data-request-access="write">
# # #         </script>
# # #     </body>
# # #     '''
    
# # # # print(mainwindow)

# # # @app.route("/register_session")
# # # def register_session():
# # #     # Клиент создает сессию при запуске
# # #     session_id = str(uuid.uuid4())
# # #     created = int(time.time())
# # #     with get_db_connection() as conn:
# # #         conn.execute(
# # #             "INSERT INTO sessions (session_id, created, authorized) VALUES (?, ?, ?)",
# # #                 (session_id, created, 0)
# # #         )
# # #         conn.commit()
# # #     return jsonify({"session_id": session_id})
    
# # #     # sessions[session_id] = {"authorized": False, "token": None}
# # #     # return jsonify({"session_id": session_id})
    
# # # @app.route("/session_status/<session_id>")
# # # def session_status(session_id):
# # #     with get_db_connection() as conn:
# # #         row = conn.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,)).fetchone()
# # #     if row:
# # #         return jsonify({
# # #             "authorized": bool(row["authorized"]),
# # #             "user": dict(row) if row["authorized"] else None
# # #         })
# # #     return jsonify({"authorized": False})

# # # # @app.route("/session_status/<session_id>")
# # # # def session_status(session_id):
# # # #     return jsonify(sessions.get(session_id, {"authorized": False}))



# # # def check_response(data):
# # #     d = data.copy()
# # #     del d['hash']
# # #     d_list = []
# # #     for key in sorted(d.keys()):
# # #         if d[key] != None:
# # #             d_list.append(key + '=' + d[key])
# # #     data_string = bytes('\n'.join(d_list), 'utf-8')

# # #     secret_key = hashlib.sha256(app.config['TELEGRAM_BOT_TOKEN'].encode('utf-8')).digest()
# # #     hmac_string = hmac.new(secret_key, data_string, hashlib.sha256).hexdigest()
# # #     return hmac_string == data['hash']


# # # @app.route('/login/telegram')
# # # def login_telegram():
# # #     print(request.url)
# # #     session_id = request.args.get("session_id") # Передается клиентом
# # #     if not session_id:
# # #         return "Session ID is required", 400
    
# # #     with get_db_connection() as conn:
# # #         row = conn.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,)).fetchone()
# # #         if not row:
# # #             return "Unknown session", 400
    
    
    
    
# # #     data = {
# # #         'id': request.args.get('id', None),
# # #         'first_name': request.args.get('first_name', None),
# # #         'last_name': request.args.get('last_name', None),
# # #         'username': request.args.get('username', None),
# # #         'photo_url': request.args.get('photo_url', None),
# # #         'auth_date': request.args.get('auth_date', None),
# # #         'hash': request.args.get('hash', None)
# # #     }
    
# # #     # Проверка хэша
# # #     # if not check_response(data):
# # #         # return "Authorization failed", 403
    
# # #     # Привязка пользователя к сессии
    
# # #     if check_response(data):
# # #         user_id = data.get("id")
# # #         token = hashlib.sha256((data["id"] + data["auth_date"]).encode()).hexdigest()
# # #         created = int(time.time())
# # #         with get_db_connection() as conn:
# # #             # Проверка существующей сессии для пользователя
# # #             existing = conn.execute("SELECT * FROM sessions WHERE user_id = ?", (user_id,)).fetchone()
# # #             if existing:
# # #                 return f"User {user_id} already has an active session ({existing['session_id']})", 403

# # #             conn.execute("""
# # #                 UPDATE sessions
# # #                 SET user_id=?, token=?, authorized=?, created=?
# # #                 WHERE session_id=?
# # #             """, (user_id, token, 1, created, session_id))
# # #             conn.commit()
            
# # #         print("Data from Telegram:", data)
# # #         return f"{user_id} is Authorized! You can close this window.\n session {session_id}"
# # #     else:
# # #         return 'Authorization failed', 403
    
# # # @app.route("/logout", methods=["POST"])
# # # def logout():
# # #     session_id = request.json.get("session_id")
# # #     with get_db_connection() as conn:
# # #         conn.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))
# # #         conn.commit()
# # #     return jsonify({"message": "Logged out"})


# # # if __name__ == "__main__":
# # #     app.run(host='0.0.0.0', port=8000, debug=True)
# # #         # # Проверка на повторную сессию
# # #         # if user_id in user_sessions:
# # #         #     old_session = user_sessions.get(user_id)
# # #         #     return f"User {user_id} already has an active session ({old_session})", 403
        
# # #         # # Authorize user
# # #         # print("Data from Telegram:", data)
        
# # #         # # token = secrets.token_hex(16)
# # #         # token = hashlib.sha256((data["id"] + data["auth_date"]).encode()).hexdigest()
# # #         # sessions[session_id] = {"authorized": True, "user": data, "token": token, "user_id": user_id}
# # #         # user_sessions[user_id] = session_id
# # #         # # return jsonify({"message": "ok", "token": token})
# # #         # return f"{user_id} is Authorized! You can close this window.\n session {session_id}"
    

# # #     # if check_response(data):
# # #     #     # Authorize user when data is locally
# # #     #     print("Data from Telegram:", data)
# # #     #     with open(f"auth_done_{data['username']}.json", "w", encoding="utf8") as f:
# # #     #         f.write(json.dumps(data, indent=2))
# # #     #     return data
# # #     # else:
# # #     #     return 'Authorization failed', 403

# # # # @app.route("/check_session/<session_id>")
# # # # def check_session(session_id):
# # # #     # Клиент опрашивает свой session_id
# # # #     return jsonify(sessions.get(session_id, {"authorized": False}))

# # # # @app.route("/telegram_callback", methods=["GET"])
# # # # def telegram_callback():
# # # #     user_data = request.args.to_dict()
# # # #     print("Telegram callback received:", user_data)
    
# # # #     # Тут можно сигнализировать PyQt о том, что авторизация прошла
# # # #     # Например, через файл, очередь или простой глобальный флаг
# # # #     with open("auth_done.txt", "w") as f:
# # # #         f.write("ok")
    
# # # #     return "You can close this window now"




    