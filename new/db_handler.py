import database

COURSE_CACHE = {}

def refresh_course_cache():
    """تحديث ذاكرة المواد من قاعدة البيانات"""
    global COURSE_CACHE
    COURSE_CACHE = database.fetch_courses_with_sections()

# تحديث الكاش عند البدء
refresh_course_cache()

def create_user_account(student_id, email, password, role, display_name=None, mobile=None):
    conn = database.get_connection()
    cur = conn.cursor()
    
    # التحقق من وجود المستخدم
    cur.execute("SELECT user_id FROM users WHERE student_id = ?", (student_id,))
    row = cur.fetchone()
    
    if row:
        cur.execute("""
            UPDATE users SET email=?, password_hash=?, role=?, display_name=?, mobile=?
            WHERE student_id=?
        """, (email, password, role, display_name, mobile, student_id))
    else:
        cur.execute("""
            INSERT INTO users (student_id, email, password_hash, role, display_name, mobile)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, email, password, role, display_name, mobile))
    
    conn.commit()
    conn.close()

def db_login(academic_id, password):
    """دالة تسجيل الدخول"""
    conn = database.get_connection()
    cur = conn.cursor()
    
    # جلب بيانات المستخدم والطالب (إن وجد)
    query = """
        SELECT u.role, u.password_hash, 
               COALESCE(s.name, u.display_name), 
               COALESCE(s.email, u.email),
               s.program, s.level
        FROM users u
        LEFT JOIN students s ON u.student_id = s.student_id
        WHERE u.student_id = ?
    """
    cur.execute(query, (academic_id,))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return None
        
    role, stored_pass, name, email, program, level = row
    
    if stored_pass != password: # في الواقع يجب استخدام التشفير هنا
        return None
        
    return {
        "id": academic_id,
        "role": role,
        "name": name,
        "email": email,
        "program": program,
        "level": level
    }

# إنشاء حساب الأدمن الافتراضي
create_user_account("admin", "admin@univ.edu", "admin", "hod", "Head of Department")