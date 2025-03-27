from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime, timedelta
import bcrypt

app = Flask(__name__)
app.secret_key = 'XasUS*#$)(*123'

DATABASE = 'lib_manage.db'


def get_db():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # 允许通过列名访问数据
    return conn


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role")

    conn = get_db()
    cursor = conn.cursor()

    # 从数据库中获取用户的哈希密码
    cursor.execute("SELECT * FROM users WHERE username = ? AND role = ?", (username, role))
    user = cursor.fetchone()

    conn.close()

    if user:
        # 从查询结果中获取存储的哈希密码，并确保它是字节串
        stored_password = user["password"]
        if isinstance(stored_password, str):  # 如果是字符串，转为字节串
            stored_password = stored_password.encode('utf-8')

        # 使用 bcrypt 验证输入的密码和哈希密码是否匹配
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            session['username'] = username
            if role == "Librarian":
                return render_template("libr_frontpage.html", username=username)
            elif role == "Student":
                return render_template("stud_frontpage.html", username=username)

    # 登录失败
    return render_template("index.html", error="Invalid username, password or role")


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 获取表单数据
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role")

    # 哈希密码
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # 将数据插入数据库
    conn = get_db()
    cursor = conn.cursor()

    # 插入新用户，保存哈希后的密码
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
    conn.commit()
    conn.close()

    # 注册成功后可以重定向到登录页或显示注册成功的页面
    return render_template("index.html", message="Registration successful, please log in")

@app.route('/books')
def books():  # put application's code here
    username = session.get('username')
    conn = get_db()
    cursor = conn.cursor()

    # 从数据库中查询所有书籍数据
    cursor.execute("""
        SELECT books.book_id, books.title, books.author, books.publication_year, books.isbn, books.genre, 
               book_inventory.quantity, book_inventory.availability
        FROM books
        LEFT JOIN book_inventory ON books.book_id = book_inventory.item_id_fk
    """)
    books = cursor.fetchall()  # 获取用户数据
    cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    role = user['role'] if user else None

    borrowed_date = datetime.now().date()
    due_date = borrowed_date + timedelta(days=14)
    return_date = datetime.now().date()

    conn.close()

    # 将 books 数据传递到模板
    return render_template("books.html", books=books, role=role, username=username,
                           borrowed_date=borrowed_date, due_date=due_date, return_date=return_date)


@app.route('/stu_books')
def stu_books():  # put application's code here
    username = session.get('username')
    conn = get_db()
    cursor = conn.cursor()

    # 从数据库中查询所有书籍数据
    cursor.execute("""
        SELECT books.book_id, books.title, books.author, books.publication_year, books.isbn, books.genre, 
               book_inventory.quantity, book_inventory.availability
        FROM books
        LEFT JOIN book_inventory ON books.book_id = book_inventory.item_id_fk
    """)
    books = cursor.fetchall()  # 获取用户数据
    cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    role = user['role'] if user else None

    borrowed_date = datetime.now().date()
    due_date = borrowed_date + timedelta(days=14)
    return_date = datetime.now().date()

    conn.close()

    # 将 books 数据传递到模板
    return render_template("stu_books.html", books=books, role=role, username=username,
                           borrowed_date=borrowed_date, due_date=due_date, return_date=return_date)


@app.route('/e_resources')
def e_resources():  # put application's code here
    conn =get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM digital_resources")
    esources = cursor.fetchall()

    conn.close()

    return render_template("e_resources.html", esources=esources)

@app.route('/eresource_search', methods=['GET', 'POST'])
def eresource_search():
    search_query = request.form.get("search")  # 获取搜索框的值

    # 连接数据库
    conn = get_db()
    cursor = conn.cursor()


    # 使用 LIKE 语句来进行模糊搜索
    sql = '''
        SELECT * FROM digital_resources
        WHERE title LIKE ? OR resource_type LIKE ?
    '''
    search_term = f"%{search_query}%"
    cursor.execute(sql, (search_term, search_term))
    esources = cursor.fetchall()

    conn.close()

    return render_template("e_resources.html", esources=esources)  # 渲染书籍列表页面


@app.route('/stu_e_resources')
def stu_e_resources():  # put application's code here
    conn =get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM digital_resources")
    esources = cursor.fetchall()

    conn.close()

    return render_template("stu_e_resources.html", esources=esources)


@app.route('/stueresource_search', methods=['GET', 'POST'])
def stueresource_search():
    search_query = request.form.get("search")  # 获取搜索框的值

    # 连接数据库
    conn = get_db()
    cursor = conn.cursor()


    # 使用 LIKE 语句来进行模糊搜索
    sql = '''
        SELECT * FROM digital_resources
        WHERE title LIKE ? OR resource_type LIKE ?
    '''
    search_term = f"%{search_query}%"
    cursor.execute(sql, (search_term, search_term))
    esources = cursor.fetchall()

    conn.close()

    return render_template("stu_e_resources.html", esources=esources)  # 渲染书籍列表页面


@app.route('/users')
def users():  # put application's code here
    conn =get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template("users.html", users=users)


@app.route('/user_search', methods=['GET', 'POST'])
def user_search():
    search_query = request.form.get("search")  # 获取搜索框的值

    # 连接数据库
    conn = get_db()
    cursor = conn.cursor()


    # 使用 LIKE 语句来进行模糊搜索
    sql = '''
        SELECT * FROM users
        WHERE user_id LIKE ? OR username LIKE ? OR role LIKE ?
    '''
    search_term = f"%{search_query}%"
    cursor.execute(sql, (search_term, search_term, search_term))
    users = cursor.fetchall()

    conn.close()

    return render_template("users.html", users=users)  # 渲染书籍列表页面

@app.route('/books_manage')
def books_manage():  # put application's code here
    conn = get_db()
    cursor = conn.cursor()

    # 从数据库中查询所有书籍数据
    cursor.execute("""
        SELECT books.book_id, books.title, books.author, books.publication_year, books.isbn, books.genre, 
               book_inventory.quantity, book_inventory.availability
        FROM books
        LEFT JOIN book_inventory ON books.book_id = book_inventory.item_id_fk
    """)

    books = cursor.fetchall()  # 获取所有书籍记录

    conn.close()

    # 将 books 数据传递到模板
    return render_template("books_manage.html", books=books)


@app.route('/bookma_search', methods=['GET', 'POST'])
def bookma_search():
    search_query = request.form.get("search")  # 获取搜索框的值

    # 连接数据库
    conn = get_db()
    cursor = conn.cursor()

    # 构建 SQL 查询语句
    # 使用 LIKE 语句来进行模糊搜索
    sql = '''
        SELECT books.*, book_inventory.quantity, book_inventory.availability 
        FROM books
        LEFT JOIN book_inventory ON books.book_id = book_inventory.item_id_fk
        WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? OR genre LIKE ?
    '''
    search_term = f"%{search_query}%"
    cursor.execute(sql, (search_term, search_term, search_term, search_term))
    books = cursor.fetchall()

    conn.close()

    return render_template("books_manage.html", books=books)  # 渲染书籍列表页面


@app.route('/borrowing_status')
def borrowing_status():  # put application's code here
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT borrowing_records.record_id, borrowing_records.borrowed_date, borrowing_records.due_date, borrowing_records.return_date, borrowing_records.status,       
                books.title,
                users.username
        FROM borrowing_records
        JOIN books ON borrowing_records.book_id = books.book_id
        JOIN users ON borrowing_records.user_id = users.user_id;
    """)
    records = cursor.fetchall()

    conn.close()

    return render_template("borrowing_records.html", records=records)

@app.route('/record_search', methods=['GET', 'POST'])
def record_search():
    search_query = request.form.get("search")  # 获取搜索框的值

    # 连接数据库
    conn = get_db()
    cursor = conn.cursor()

    # 构建 SQL 查询语句
    # 使用 LIKE 语句来进行模糊搜索
    sql = '''
        SELECT borrowing_records.record_id, borrowing_records.borrowed_date, borrowing_records.due_date, borrowing_records.return_date, borrowing_records.status,       
                books.title,
                users.username
        FROM borrowing_records
        JOIN books ON borrowing_records.book_id = books.book_id
        JOIN users ON borrowing_records.user_id = users.user_id
        WHERE books.title LIKE ? OR users.username LIKE ? OR borrowing_records.record_id LIKE ?
    '''
    search_term = f"%{search_query}%"
    cursor.execute(sql, (search_term, search_term, search_term))
    records = cursor.fetchall()

    conn.close()

    return render_template("borrowing_records.html", records=records)  # 渲染书籍列表页面



@app.route('/personal_center')
def personal_center():  # put application's code here
    username = session.get('username')
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    users = cursor.fetchall()

    cursor.execute("""
        SELECT borrowing_records.*, books.title FROM borrowing_records
        JOIN users ON borrowing_records.user_id = users.user_id
        JOIN books ON borrowing_records.book_id = books.book_id
        WHERE users.username=?
    """, (username,))
    borrowing_records = cursor.fetchall()

    conn.close()

    return render_template("personal_center.html", users=users, username=username, borrowing_records=borrowing_records)


@app.route('/stu_personal_center')
def stu_personal_center():  # put application's code here
    username = session.get('username')
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    users = cursor.fetchall()

    cursor.execute("""
        SELECT borrowing_records.*, books.title FROM borrowing_records
        JOIN users ON borrowing_records.user_id = users.user_id
        JOIN books ON borrowing_records.book_id = books.book_id
        WHERE users.username=?
    """, (username,))
    borrowing_records = cursor.fetchall()

    conn.close()

    return render_template("stu_personal_center.html", users=users, username=username, borrowing_records=borrowing_records)


@app.route('/user_add', methods=['POST'])
def user_add():  # put application's code here
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))

    conn.commit()
    conn.close()

    return redirect(url_for('users'))

@app.route('/user_edit', methods=['POST'])
def user_edit():
    # 获取表单中的数据
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')

    # 如果密码为空，保持原密码
    if password:
        # 如果有新密码，使用 bcrypt 对密码加密
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    else:
        # 否则使用旧密码（这个步骤假设你在数据库中获取了旧密码并在编辑时不做修改）
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        hashed_password = user[0]  # 获取旧密码

    # 更新数据库中的用户信息
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ?, password = ?, role = ? WHERE user_id = ?",
                   (username, hashed_password, role, user_id))
    conn.commit()
    conn.close()

    return redirect(url_for('users'))


@app.route('/user_delete', methods=['POST'])
def user_delete():
    # 获取表单中的数据
    user_id = request.form.get('user_id')

    # 更新数据库中的用户信息
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

    # 重定向
    return redirect(url_for('users'))


@app.route('/book_add', methods=['POST'])
def book_add():  # put application's code here
    title = request.form['title']
    author = request.form['author']
    publication_year = request.form['publication_year']
    isbn = request.form['isbn']
    genre = request.form['genre']
    quantity = request.form['quantity']
    availability = request.form['availability']

    quantity = int(quantity)
    availability = "Available" if quantity > 0 else "Not Available"

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO books (title, author, publication_year, isbn, genre) VALUES (?, ?, ?, ?, ?)",
                   (title, author, publication_year, isbn, genre))
    book_id = cursor.lastrowid
    cursor.execute("INSERT INTO book_inventory (item_id_fk, quantity, availability) VALUES (?, ?, ?)",
                   (book_id, quantity, availability))
    conn.commit()
    conn.close()

    return redirect(url_for('books_manage'))

@app.route('/book_edit', methods=['POST'])
def book_edit():
    book_id = request.form['book_id']
    title = request.form['title']
    author = request.form['author']
    publication_year = request.form['publication_year']
    isbn = request.form['isbn']
    genre = request.form['genre']
    quantity = request.form['quantity']
    availability = request.form['availability']

    quantity = int(quantity)
    availability = "Available" if quantity > 0 else "Not Available"

    # 更新数据库中的用户信息
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title = ?, author = ?, publication_year = ?, isbn = ?, genre = ? WHERE book_id = ?",
                   (title, author, publication_year, isbn, genre, book_id))

    cursor.execute("UPDATE book_inventory SET quantity = ?, availability = ? WHERE item_id_fk = ?",
                   (quantity, availability, book_id))
    conn.commit()
    conn.close()

    # 重定向
    return redirect(url_for('books_manage'))

@app.route('/book_delete', methods=['POST'])
def book_delete():
    # 获取表单中的数据
    book_id = request.form.get('book_id')

    # 更新数据库中的用户信息
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
    cursor.execute("DELETE FROM book_inventory WHERE item_id_fk = ?", (book_id,))

    conn.commit()
    conn.close()

    # 重定向
    return redirect(url_for('books_manage'))

@app.route('/book_search', methods=['GET', 'POST'])
def book_search():
    search_query = request.form.get("search")  # 获取搜索框的值

    # 连接数据库
    conn = get_db()
    cursor = conn.cursor()

    # 构建 SQL 查询语句
    # 使用 LIKE 语句来进行模糊搜索
    sql = '''
        SELECT books.*, book_inventory.quantity, book_inventory.availability 
        FROM books
        LEFT JOIN book_inventory ON books.book_id = book_inventory.item_id_fk
        WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? OR genre LIKE ?
    '''
    search_term = f"%{search_query}%"
    cursor.execute(sql, (search_term, search_term, search_term, search_term))
    books = cursor.fetchall()

    conn.close()

    return render_template("books.html", books=books)  # 渲染书籍列表页面


@app.route('/stubook_search', methods=['GET', 'POST'])
def stubook_search():
    search_query = request.form.get("search")  # 获取搜索框的值

    # 连接数据库
    conn = get_db()
    cursor = conn.cursor()

    # 构建 SQL 查询语句
    # 使用 LIKE 语句来进行模糊搜索
    sql = '''
        SELECT books.*, book_inventory.quantity, book_inventory.availability 
        FROM books
        LEFT JOIN book_inventory ON books.book_id = book_inventory.item_id_fk
        WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? OR genre LIKE ?
    '''
    search_term = f"%{search_query}%"
    cursor.execute(sql, (search_term, search_term, search_term, search_term))
    books = cursor.fetchall()

    conn.close()

    return render_template("stu_books.html", books=books)  # 渲染书籍列表页面


@app.route('/personal_edit', methods=['POST'])
def personal_edit():
    # 获取表单中的数据
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    password = request.form.get('password')

    # 如果密码为空，保持原密码
    if password:
        # 如果有新密码，使用 bcrypt 对密码加密
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    else:
        # 否则使用旧密码（这个步骤假设你在数据库中获取了旧密码并在编辑时不做修改）
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        hashed_password = user[0]  # 获取旧密码

    # 更新数据库中的用户信息
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ?, password = ? WHERE user_id = ?",
                   (username, hashed_password, user_id))
    conn.commit()
    conn.close()

    session['username'] = username

    # 重定向
    return redirect(url_for('personal_center'))


@app.route('/stu_personal_edit', methods=['POST'])
def stu_personal_edit():
    # 获取表单中的数据
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    password = request.form.get('password')

    # 如果密码为空，保持原密码
    if password:
        # 如果有新密码，使用 bcrypt 对密码加密
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    else:
        # 否则使用旧密码（这个步骤假设你在数据库中获取了旧密码并在编辑时不做修改）
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        hashed_password = user[0]  # 获取旧密码

    # 更新数据库中的用户信息
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ?, password = ? WHERE user_id = ?",
                   (username, hashed_password, user_id))
    conn.commit()
    conn.close()

    session['username'] = username

    # 重定向
    return redirect(url_for('stu_personal_center'))


@app.route('/book_borrow', methods=['POST'])
def book_borrow():  # put application's code here
    book_id = request.form.get('book_id')
    username = request.form.get('username')
    borrowed_date = request.form.get('borrowed_date')
    due_date = request.form.get('due_date')


    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE book_inventory SET quantity = quantity - 1 WHERE item_id_fk = ?", (book_id,))

    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id_row = cursor.fetchone()
    if user_id_row:
        user_id = user_id_row[0]
    else:
        conn.close()
        return "User not found.", 404

    cursor.execute("INSERT INTO borrowing_records (book_id, user_id, borrowed_date, due_date, return_date, status) VALUES (?, ?, ?, ?, ?, ?)",
                   (book_id, user_id, borrowed_date, due_date, None, 'borrowed'))
    conn.commit()
    conn.close()

    return redirect(url_for('books'))


@app.route('/stu_book_borrow', methods=['POST'])
def stu_book_borrow():  # put application's code here
    return redirect(url_for('stu_books'))


@app.route('/book_return', methods=['POST'])
def book_return():  # put application's code here
    book_id = request.form.get('book_id')
    username = request.form.get('username')
    return_date = request.form.get('return_date')


    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE book_inventory SET quantity = quantity + 1 WHERE item_id_fk = ?", (book_id,))

    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id_row = cursor.fetchone()
    if user_id_row:
        user_id = user_id_row[0]
    else:
        conn.close()
        return "User not found.", 404

    cursor.execute("UPDATE borrowing_records SET return_date = ? WHERE book_id = ? AND user_id = ?", (return_date, book_id, user_id))
    conn.commit()
    conn.close()

    return redirect(url_for('books'))


@app.route('/analyze')
def analyze():  # put application's code here
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT books.genre, 
               COALESCE(COUNT(borrowing_records.book_id), 0) AS borrow_count
        FROM books
        LEFT JOIN borrowing_records 
            ON borrowing_records.book_id = books.book_id
        GROUP BY books.genre
        ORDER BY borrow_count DESC;
    """)

    genrecords = cursor.fetchall()

    cursor.execute("""
        SELECT books.author, 
               COALESCE(COUNT(borrowing_records.book_id), 0) AS borrow_count
        FROM books
        LEFT JOIN borrowing_records 
            ON borrowing_records.book_id = books.book_id
        GROUP BY books.author
        ORDER BY borrow_count DESC;
    """)

    autrecords = cursor.fetchall()

    cursor.execute("""
        SELECT books.publication_year, 
               COALESCE(COUNT(borrowing_records.book_id), 0) AS borrow_count
        FROM books
        LEFT JOIN borrowing_records 
            ON borrowing_records.book_id = books.book_id
        GROUP BY books.publication_year
        ORDER BY borrow_count DESC;
    """)

    pubrecords = cursor.fetchall()

    conn.close()

    genrecords = [{"category": record[0], "borrow_count": record[1]} for record in genrecords]
    autrecords = [{"category": record[0], "borrow_count": record[1]} for record in autrecords]
    pubrecords = [{"category": record[0], "borrow_count": record[1]} for record in pubrecords]

    return render_template("analyze.html", genrecords=genrecords, autrecords=autrecords, pubrecords=pubrecords)


if __name__ == '__main__':
    app.run()
