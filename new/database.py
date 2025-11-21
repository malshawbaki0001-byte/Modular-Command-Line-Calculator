import sqlite3

DB_NAME = "plans.db"
ALLOWED_PROGRAMS = ("Computer", "Communications", "Power", "Biomedical")

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def create_database():
    conn = get_connection()
    cur = conn.cursor()

    # جداول المواد
    cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            credits INTEGER NOT NULL CHECK (credits > 0),
            lecture_hours INTEGER NOT NULL DEFAULT 0,
            lab_hours INTEGER DEFAULT 0,
            max_capacity INTEGER NOT NULL DEFAULT 30
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS prerequisites (
            course_code TEXT NOT NULL,
            prereq_code TEXT NOT NULL,
            PRIMARY KEY (course_code, prereq_code),
            FOREIGN KEY (course_code) REFERENCES courses(course_code) ON DELETE CASCADE
        );
    """)

    # جداول الشعب
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sections (
            section_id TEXT PRIMARY KEY,
            course_code TEXT NOT NULL,
            instructor TEXT NOT NULL,
            start_time INTEGER NOT NULL,
            end_time INTEGER NOT NULL,
            hall TEXT NOT NULL,
            max_capacity INTEGER NOT NULL,
            current_enrollment INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (course_code) REFERENCES courses(course_code) ON DELETE CASCADE
        );
    """)

    # جداول الطلاب والمستخدمين
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            program TEXT NOT NULL,
            level TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            role TEXT,
            display_name TEXT,
            mobile TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            course_code TEXT NOT NULL,
            grade TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        );
    """)

    # جدول التسجيل (تم تعديله ليشمل section_id)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            reg_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            course_code TEXT NOT NULL,
            section_id TEXT NOT NULL,
            status TEXT DEFAULT 'Registered',
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (section_id) REFERENCES sections(section_id)
        );
    """)
    
    conn.commit()
    conn.close()

# --- دوال الإدخال والتعديل ---

def add_student(student_id, name, email, program, level):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO students (student_id, name, email, program, level) VALUES (?, ?, ?, ?, ?)",
                    (student_id, name, email, program, level))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def upsert_course(course_code, name, credits, prereqs_list):
    conn = get_connection()
    cur = conn.cursor()
    # إضافة المادة
    cur.execute("""
        INSERT INTO courses (course_code, name, credits) VALUES (?, ?, ?)
        ON CONFLICT(course_code) DO UPDATE SET name=excluded.name, credits=excluded.credits
    """, (course_code, name, credits))
    
    # تحديث المتطلبات (حذف القديم وإضافة الجديد)
    cur.execute("DELETE FROM prerequisites WHERE course_code = ?", (course_code,))
    for pre in prereqs_list:
        if pre.strip():
            cur.execute("INSERT INTO prerequisites (course_code, prereq_code) VALUES (?, ?)", (course_code, pre.strip()))
    
    conn.commit()
    conn.close()

def delete_course(course_code):
    conn = get_connection()
    conn.execute("DELETE FROM courses WHERE course_code = ?", (course_code,))
    conn.commit()
    conn.close()

def upsert_section(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sections (section_id, course_code, instructor, start_time, end_time, hall, max_capacity, current_enrollment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(section_id) DO UPDATE SET
            instructor=excluded.instructor, start_time=excluded.start_time, end_time=excluded.end_time,
            hall=excluded.hall, max_capacity=excluded.max_capacity
    """, (data['id'], data['course_code'], data['instructor'], data['start'], data['end'], data['hall'], data['max_capacity'], 0))
    conn.commit()
    conn.close()

def delete_section(section_id):
    conn = get_connection()
    conn.execute("DELETE FROM sections WHERE section_id = ?", (section_id,))
    conn.commit()
    conn.close()

def update_section_stats(section_id, change):
    conn = get_connection()
    conn.execute("UPDATE sections SET current_enrollment = current_enrollment + ? WHERE section_id = ?", (change, section_id))
    conn.commit()
    conn.close()

# --- دوال الجلب (Data Fetching) ---

def fetch_courses_with_sections():
    conn = get_connection()
    cur = conn.cursor()
    
    # جلب المواد
    courses = {}
    cur.execute("SELECT course_code, name, credits FROM courses")
    for row in cur.fetchall():
        courses[row[0]] = {
            'name': row[1], 
            'credit_hours': row[2], 
            'prerequisites': [], 
            'sections': []
        }
    
    # جلب المتطلبات
    cur.execute("SELECT course_code, prereq_code FROM prerequisites")
    for row in cur.fetchall():
        if row[0] in courses:
            courses[row[0]]['prerequisites'].append(row[1])
            
    # جلب الشعب
    cur.execute("SELECT section_id, course_code, instructor, start_time, end_time, hall, max_capacity, current_enrollment FROM sections")
    for row in cur.fetchall():
        c_code = row[1]
        if c_code in courses:
            courses[c_code]['sections'].append({
                'id': row[0], 'instructor': row[2], 'start': row[3], 'end': row[4],
                'hall': row[5], 'max_capacity': row[6], 'current_enrollment': row[7],
                'course_code': c_code, # مهم للربط
                'course_name': courses[c_code]['name'],
                'credit_hours': courses[c_code]['credit_hours'],
                'prerequisites': courses[c_code]['prerequisites']
            })
            
    conn.close()
    return courses

def get_student_transcript(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT course_code FROM transcripts WHERE student_id = ?", (student_id,))
    passed = [row[0] for row in cur.fetchall()]
    conn.close()
    return passed

def get_student_schedule(student_id):
    conn = get_connection()
    cur = conn.cursor()
    # ربط جدول التسجيل مع الشعب والمواد لجلب كامل التفاصيل
    query = """
        SELECT s.section_id, s.course_code, c.name, s.instructor, s.start_time, s.end_time, s.hall, c.credits
        FROM registrations r
        JOIN sections s ON r.section_id = s.section_id
        JOIN courses c ON s.course_code = c.course_code
        WHERE r.student_id = ?
    """
    cur.execute(query, (student_id,))
    schedule = []
    for row in cur.fetchall():
        schedule.append({
            'id': row[0], 'course_code': row[1], 'course_name': row[2],
            'instructor': row[3], 'start': row[4], 'end': row[5],
            'hall': row[6], 'credit_hours': row[7]
        })
    conn.close()
    return schedule

def register_student(student_id, section_id, course_code):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO registrations (student_id, section_id, course_code) VALUES (?, ?, ?)", 
                     (student_id, section_id, course_code))
        conn.execute("UPDATE sections SET current_enrollment = current_enrollment + 1 WHERE section_id = ?", (section_id,))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()

def unregister_student(student_id, section_id):
    conn = get_connection()
    try:
        conn.execute("DELETE FROM registrations WHERE student_id = ? AND section_id = ?", (student_id, section_id))
        conn.execute("UPDATE sections SET current_enrollment = current_enrollment - 1 WHERE section_id = ?", (section_id,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# إنشاء قاعدة البيانات عند الاستيراد
create_database()