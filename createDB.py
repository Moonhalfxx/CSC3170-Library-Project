import sqlite3
import bcrypt

# 创建数据库和表
conn = sqlite3.connect('lib_manage.db')
cursor = conn.cursor()

# 创建user表
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )''')


# 创建books表
cursor.execute("""CREATE TABLE books (
                    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publication_year INTEGER,
                    isbn TEXT UNIQUE,
                    genre TEXT
                )""")

# 创建borrowing_records表
cursor.execute("""CREATE TABLE borrowing_records (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    borrowed_date DATE NOT NULL,
                    due_date DATE NOT NULL,
                    return_date DATE,
                    status TEXT NOT NULL CHECK (status IN ('borrowed', 'returned', 'overdue')),
                    FOREIGN KEY (book_id) REFERENCES books(book_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )""")

# 创建digital_resources表
cursor.execute("""CREATE TABLE digital_resources (
                    resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    resource_type TEXT CHECK(resource_type IN ('eBook', 'Database', 'Journal')),
                    access_url TEXT NOT NULL,
                    publication_year INTEGER
                )""")

# 创建book_inventory表
cursor.execute("""CREATE TABLE book_inventory (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id_fk INTEGER,
                    quantity INTEGER,
                    availability TEXT CHECK(availability IN ('Available', 'Not Available')),
                    FOREIGN KEY(item_id_fk) REFERENCES books(book_id)
                )""")


# 在user表中插入测试数据
users_data = [
    ('admin', '123', 'Librarian'),
    ('moon', '123', 'Librarian'),
    ('librarian3', '1zcgv23', 'Librarian'),
    ('librarian4', '123hgf', 'Librarian'),
    ('librarian5', '123sfdg', 'Librarian'),
    ('librarian6', '1274533', 'Librarian'),
    ('librarian7', '12cbvn3', 'Librarian'),
    ('librarian8', '123', 'Librarian'),
    ('librarian9', '123', 'Librarian'),
    ('librarian10', '123', 'Librarian'),
    ('user', '12fdg3','Student'),
    ('mumu', '12asd3', 'Student'),
    ('mumu1', '1278533', 'Student'),
    ('mumu2', '12dhg3', 'Student'),
    ('mumu3', '18754323', 'Student'),
    ('mumu4', '1785323', 'Student'),
    ('student5', '12785363', 'Student'),
    ('student6', '12785343', 'Student'),
    ('student7', '12fghfgh3', 'Student'),
    ('student8', '1275233', 'Student'),
    ('student9', '12323457', 'Student'),
    ('student10', '12765433', 'Student'),
    ('student11', '12786543', 'Student'),
    ('student12', '12fdg3', 'Student'),
    ('student13', '125543', 'Student'),
    ('student14', '12231353', 'Student'),
    ('student15', '128883', 'Student'),
    ('student16', '524123', 'Student'),
    ('student17', '123234823', 'Student'),
    ('student18', '198923', 'Student'),
    ('student19', '1212453', 'Student'),
    ('student20', '1243656423', 'Student'),
    ('student21', '12773', 'Student'),
    ('student22', '12345645', 'Student'),
    ('student23', '123', 'Student'),
    ('student24', '123', 'Student'),
    ('student25', '15523', 'Student'),
    ('student26', '145323', 'Student'),
    ('student27', '123', 'Student'),
    ('student28', '12123133', 'Student'),
    ('student29', '123', 'Student'),
    ('student30', '123', 'Student'),
    ('student31', '1212213', 'Student'),
    ('student32', '17823', 'Student'),
    ('student33', '125553', 'Student'),
    ('student34', '155546723', 'Student'),
    ('student35', '123777', 'Student')
]
for username, password, role in users_data:
    # 加密密码
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # 插入数据
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                   (username, hashed_password, role))

# 在books表中插入测试数据
books_data = [
    ('To Kill a Mockingbird', 'Harper Lee', 1960, '978-0-06-112008-4', 'Fiction'),
    ('1984', 'George Orwell', 1949, '978-0-452-28423-4', 'Dystopian'),
    ('Pride and Prejudice', 'Jane Austen', 1813, '978-1-85326-000-1', 'Romance'),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925, '978-0-7432-7356-5', 'Classic'),
    ('Moby Dick', 'Herman Melville', 1851, '978-0-14-243724-7', 'Adventure'),
    ('War and Peace', 'Leo Tolstoy', 1869, '978-0-14-303999-0', 'Historical Fiction'),
    ('The Catcher in the Rye', 'J.D. Salinger', 1951, '978-0-316-76948-0', 'Fiction'),
    ('Brave New World', 'Aldous Huxley', 1932, '978-0-06-085052-3', 'Dystopian'),
    ('The Hobbit', 'J.R.R. Tolkien', 1937, '978-0-618-00221-3', 'Fantasy'),
    ('The Odyssey', 'Homer', -800, '978-0-14-026886-7', 'Classic'),
    ('Jane Eyre', 'Charlotte Brontë', 1847, '978-0-14-243720-9', 'Romance'),
    ('The Picture of Dorian Gray', 'Oscar Wilde', 1890, '978-0-14-143957-0', 'Gothic'),
    ('Crime and Punishment', 'Fyodor Dostoevsky', 1866, '978-0-14-044913-6', 'Psychological Fiction'),
    ('The Divine Comedy', 'Dante Alighieri', 1320, '978-0-14-243722-3', 'Epic Poetry'),
    ('Fahrenheit 451', 'Ray Bradbury', 1953, '978-0-7432-4722-1', 'Dystopian'),
    ('The Lord of the Rings', 'J.R.R. Tolkien', 1954, '978-0-618-00223-7', 'Fantasy'),
    ('Wuthering Heights', 'Emily Brontë', 1847, '978-0-14-143955-6', 'Romance'),
    ('The Brothers Karamazov', 'Fyodor Dostoevsky', 1880, '978-0-14-044924-2', 'Philosophical Fiction'),
    ('Dracula', 'Bram Stoker', 1897, '978-0-14-143984-6', 'Gothic'),
    ('The Count of Monte Cristo', 'Alexandre Dumas', 1844, '978-0-14-044926-6', 'Adventure'),
    ('A Tale of Two Cities', 'Charles Dickens', 1859, '978-0-14-143960-0', 'Historical Fiction'),
    ('Les Misérables', 'Victor Hugo', 1862, '978-0-14-044430-8', 'Historical Fiction'),
    ('The Iliad', 'Homer', -750, '978-0-14-027536-0', 'Epic Poetry'),
    ('Don Quixote', 'Miguel de Cervantes', 1605, '978-0-14-243723-0', 'Adventure'),
    ('Anna Karenina', 'Leo Tolstoy', 1877, '978-0-14-303500-8', 'Romance'),
    ('Heart of Darkness', 'Joseph Conrad', 1899, '978-0-14-144167-2', 'Classic'),
    ('Frankenstein', 'Mary Shelley', 1818, '978-0-14-143947-1', 'Gothic'),
    ('Ulysses', 'James Joyce', 1922, '978-0-679-72256-7', 'Modernist'),
    ('Madame Bovary', 'Gustave Flaubert', 1856, '978-0-14-044912-9', 'Realism'),
    ('The Sound and the Fury', 'William Faulkner', 1929, '978-0-679-73224-5', 'Southern Gothic'),
    ('The Sun Also Rises', 'Ernest Hemingway', 1926, '978-0-7432-0736-2', 'Modernist'),
    ('The Scarlet Letter', 'Nathaniel Hawthorne', 1850, '978-0-14-243726-1', 'Classic'),
    ('Medea', 'Euripides', -431, '978-0-14-044929-7', 'Ancient Greek Tragedy'),
    ('The Grapes of Wrath', 'John Steinbeck', 1939, '978-0-14-303943-3', 'Classic'),
    ('Gone with the Wind', 'Margaret Mitchell', 1936, '978-0-684-80190-9', 'Historical Fiction'),
    ('Catch-22', 'Joseph Heller', 1961, '978-0-684-83339-9', 'Satire'),
    ('One Hundred Years of Solitude', 'Gabriel Garcia Marquez', 1967, '978-0-06-088328-7', 'Magic Realism'),
    ('Slaughterhouse-Five', 'Kurt Vonnegut', 1969, '978-0-385-31208-0', 'Science Fiction'),
    ('Beloved', 'Toni Morrison', 1987, '978-0-14-243727-8', 'Historical Fiction'),
    ('The Alchemist', 'Paulo Coelho', 1988, '978-0-06-112241-5', 'Fantasy')
]
cursor.executemany(
    "INSERT INTO books (title, author, publication_year, isbn, genre) VALUES (?, ?, ?, ?, ?)",
    books_data
)

# 在borrowing_records表中插入测试数据
borrowing_record_data = [
    (1, 1, '2024-01-10', '2024-01-24', '2024-01-22', 'returned'),
    (2, 2, '2024-01-12', '2024-01-26', None, 'overdue'),
    (3, 3, '2024-02-01', '2024-02-15', '2024-02-14', 'returned'),
    (4, 4, '2024-02-05', '2024-02-19', None, 'overdue'),
    (1, 5, '2024-02-08', '2024-02-22', '2024-02-21', 'returned'),
    (2, 6, '2024-03-01', '2024-03-15', None, 'overdue'),
    (5, 1, '2024-03-10', '2024-03-24', None, 'overdue'),
    (3, 2, '2024-03-12', '2024-03-26', '2024-03-25', 'returned'),
    (4, 7, '2024-04-01', '2024-04-15', None, 'overdue'),
    (5, 8, '2024-04-02', '2024-04-16', '2024-04-12', 'returned'),
    (6, 3, '2024-04-10', '2024-04-24', None, 'overdue'),
    (7, 4, '2024-04-12', '2024-04-26', '2024-04-25', 'returned'),
    (8, 5, '2024-04-20', '2024-05-04', None, 'overdue'),
    (9, 6, '2024-04-22', '2024-05-06', '2024-05-05', 'returned'),
    (10, 7, '2024-05-01', '2024-05-15', None, 'overdue'),
    (1, 8, '2024-05-02', '2024-05-16', '2024-05-10', 'returned'),
    (2, 1, '2024-05-05', '2024-05-19', None, 'overdue'),
    (3, 2, '2024-05-07', '2024-05-21', '2024-05-20', 'returned'),
    (5, 4, '2024-11-01', '2024-11-15', None, 'borrowed'),
    (20, 32, '2024-11-01', '2024-11-15', None, 'borrowed'),
    (19, 31, '2024-11-01', '2024-11-15', '2024-11-09', 'returned'),
    (15, 26, '2024-11-01', '2024-11-15', '2024-11-08', 'returned'),
    (25, 14, '2024-11-02', '2024-11-16', '2024-11-09', 'returned'),
    (20, 20, '2024-11-03', '2024-11-17', None, 'borrowed'),
    (15, 16, '2024-11-03', '2024-11-17', None, 'borrowed'),
    (15, 19, '2024-11-03', '2024-11-17', None, 'borrowed'),
    (12, 11, '2024-11-04', '2024-11-18', None, 'borrowed'),
    (22, 10, '2024-11-04', '2024-11-18', '2024-11-08', 'returned'),
    (4, 3, '2024-11-05', '2024-11-19', None, 'borrowed'),
    (19, 8, '2024-11-05', '2024-11-19', None, 'borrowed'),
    (16, 9, '2024-11-05', '2024-11-19', None, 'borrowed'),
    (23, 13, '2024-11-05', '2024-11-19', None, 'borrowed'),
    (24, 14, '2024-11-05', '2024-11-19', None, 'borrowed')
]
cursor.executemany(
    "INSERT INTO borrowing_records (book_id, user_id, borrowed_date, due_date, return_date, status) VALUES (?, ?, ?, ?, ?, ?)",
    borrowing_record_data
)

# 在digital_resources表中插入测试数据
digital_resources_data = [
    ('IEEE Xplore Digital Library', 'Database', 'https://ieeexplore.ieee.org', 2000),
    ('Nature Journal', 'Journal', 'https://www.nature.com', 1869),
    ('JSTOR', 'Database', 'https://www.jstor.org', 1995),
    ('SpringerLink', 'Database', 'https://link.springer.com', 1997),
    ('Elsevier ScienceDirect', 'Database', 'https://www.sciencedirect.com', 1997),
    ('ACM Digital Library', 'Database', 'https://dl.acm.org', 1997),
    ('Oxford Academic', 'Journal', 'https://academic.oup.com', 1681),
    ('Project MUSE', 'Database', 'https://muse.jhu.edu', 1995),
    ('Science Magazine', 'Journal', 'https://www.sciencemag.org', 1880),
    ('PubMed Central', 'Database', 'https://www.ncbi.nlm.nih.gov/pmc', 2000),
    ('ProQuest', 'Database', 'https://www.proquest.com', 1938),
    ('Wiley Online Library', 'Database', 'https://onlinelibrary.wiley.com', 1997),
    ('Cambridge Core', 'Database', 'https://www.cambridge.org/core', 2006),
    ('Taylor & Francis Online', 'Database', 'https://www.tandfonline.com', 1998),
    ('American Chemical Society (ACS) Publications', 'Database', 'https://pubs.acs.org', 1876),
    ('SAGE Journals', 'Journal', 'https://journals.sagepub.com', 1965),
    ('IEEE Spectrum', 'Journal', 'https://spectrum.ieee.org', 1964),
    ('Open Access Theses and Dissertations (OATD)', 'Database', 'https://oatd.org', 2011),
    ('Directory of Open Access Journals (DOAJ)', 'Journal', 'https://www.doaj.org', 2003),
    ('HathiTrust Digital Library', 'Database', 'https://www.hathitrust.org', 2008),
    ('BioMed Central', 'Journal', 'https://www.biomedcentral.com', 2000),
    ('ERIC (Education Resources Information Center)', 'Database', 'https://eric.ed.gov', 1966),
    ('National Academies Press', 'eBook', 'https://www.nap.edu', 1997),
    ('Gale Academic OneFile', 'Database', 'https://www.gale.com/academic/onefile', 1954),
    ('Digital Public Library of America (DPLA)', 'Database', 'https://dp.la', 2013),
    ('IEEE Spectrum Magazine', 'Journal', 'https://spectrum.ieee.org/magazine', 1964),
    ('MIT OpenCourseWare', 'eBook', 'https://ocw.mit.edu', 2002),
    ('Smithsonian Digital Library', 'Database', 'https://library.si.edu/digital-library', 2009)
]
cursor.executemany(
    "INSERT INTO digital_resources (title, resource_type, access_url, publication_year) VALUES (?, ?, ?, ?)",
    digital_resources_data
)

# 在book_inventory表中插入测试数据
book_inventory_data = [
    (1, 32, 'Available'),
    (2, 0, 'Not Available'),
    (3, 50, 'Available'),
    (4, 0, 'Not Available'),
    (5, 37, 'Available'),
    (6, 18, 'Available'),
    (7, 45, 'Available'),
    (8, 0, 'Not Available'),
    (9, 42, 'Available'),
    (10, 29, 'Available'),
    (11, 0, 'Not Available'),
    (12, 48, 'Available'),
    (13, 12, 'Available'),
    (14, 0, 'Not Available'),
    (15, 26, 'Available'),
    (16, 17, 'Available'),
    (17, 0, 'Not Available'),
    (18, 23, 'Available'),
    (19, 41, 'Available'),
    (20, 0, 'Not Available'),
    (21, 35, 'Available'),
    (22, 0, 'Not Available'),
    (23, 47, 'Available'),
    (24, 15, 'Available'),
    (25, 0, 'Not Available'),
    (26, 28, 'Available'),
    (27, 53, 'Available'),
    (28, 0, 'Not Available'),
    (29, 39, 'Available'),
    (30, 30, 'Available'),
    (31, 0, 'Not Available'),
    (32, 22, 'Available'),
    (33, 44, 'Available'),
    (34, 0, 'Not Available'),
    (35, 31, 'Available'),
    (36, 14, 'Available'),
    (37, 0, 'Not Available'),
    (38, 25, 'Available'),
    (39, 19, 'Available'),
    (40, 0, 'Not Available')
]
cursor.executemany(
    "INSERT INTO book_inventory (item_id_fk, quantity, availability) VALUES (?, ?, ?)",
    book_inventory_data
)

# 提交更改并关闭连接
conn.commit()
conn.close()
