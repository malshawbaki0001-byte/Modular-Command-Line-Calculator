import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QListWidget, QListWidgetItem, QLabel, QFrame,
    QMessageBox, QDialog, QLineEdit, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QTabWidget, QGraphicsDropShadowEffect,
    QStatusBar, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

# --- استيراد ملفات قاعدة البيانات ---
import db_handler
import database

# --- إعدادات البرنامج ---
PROGRAM_PLANS = {
    'Computer': ['CS101', 'MATH201', 'ENGR101', 'CIRC210', 'MATH301'],
    'Communications': ['CS101', 'MATH201', 'ENGR101', 'CIRC210', 'COMM310'],
    'Power': ['CS101', 'MATH201', 'ENGR101', 'CIRC210', 'MATH301'],
    'Biomedical': ['CS101', 'MATH201', 'CIRC210', 'MATH301']
}

# --- الأنماط (Styles) ---
LIGHT_MODE_QSS = """
QDialog, QWidget { background-color: #f0f2f5; font-family: "Segoe UI", "Arial", sans-serif; color: #333; }
QFrame[class="card"], QWidget[class="card"] { background-color: #ffffff; border-radius: 10px; border: 1px solid #e0e0e0; }
QLabel { font-size: 14px; font-weight: bold; color: #333; }
QLineEdit, QComboBox { padding: 8px; border: 1px solid #ccc; border-radius: 5px; background: #fff; color: #333; }
QPushButton { background-color: #007bff; color: white; padding: 10px; border-radius: 5px; border: none; font-weight: bold; }
QPushButton:hover { background-color: #0056b3; }
QPushButton[class="danger"] { background-color: #dc3545; }
QPushButton[class="success"] { background-color: #28a745; }
QPushButton[class="theme_btn"] { background-color: #6c757d; min-width: 30px; }
QTableWidget { background-color: white; gridline-color: #eee; border: 1px solid #ccc; }
QHeaderView::section { background-color: #f1f1f1; padding: 5px; border: none; border-bottom: 1px solid #ccc; }
"""

DARK_MODE_QSS = """
QDialog, QWidget { background-color: #2b2b2b; font-family: "Segoe UI", "Arial", sans-serif; color: #f0f0f0; }
QFrame[class="card"], QWidget[class="card"] { background-color: #3c3c3c; border-radius: 10px; border: 1px solid #555; }
QLabel { font-size: 14px; font-weight: bold; color: #f0f0f0; }
QLineEdit, QComboBox { padding: 8px; border: 1px solid #555; border-radius: 5px; background: #444; color: #fff; }
QPushButton { background-color: #007bff; color: white; padding: 10px; border-radius: 5px; border: none; font-weight: bold; }
QPushButton[class="theme_btn"] { background-color: #555; min-width: 30px; }
QTableWidget { background-color: #333; gridline-color: #444; border: 1px solid #555; color: #fff; }
QHeaderView::section { background-color: #444; padding: 5px; border: none; border-bottom: 1px solid #555; color: #fff; }
"""

def apply_shadow(widget):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(15)
    shadow.setColor(QColor(0, 0, 0, 50))
    shadow.setOffset(0, 4)
    widget.setGraphicsEffect(shadow)

# --- نافذة إنشاء الحساب ---
class RegisterWindow(QDialog):
    def __init__(self, role='student', parent=None):
        super().__init__(parent)
        self.role = role
        self.setWindowTitle(f'إنشاء حساب {role}')
        self.setFixedSize(400, 500)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        layout = QVBoxLayout(self)
        card = QWidget(); card.setProperty("class", "card")
        c_layout = QVBoxLayout(card)
        
        form = QFormLayout()
        self.name_inp = QLineEdit()
        self.email_inp = QLineEdit()
        self.mobile_inp = QLineEdit()
        
        form.addRow("الاسم:", self.name_inp)
        form.addRow("البريد:", self.email_inp)
        form.addRow("الجوال:", self.mobile_inp)
        
        if role == 'student':
            self.prog_combo = QComboBox()
            self.prog_combo.addItems(PROGRAM_PLANS.keys())
            self.lvl_combo = QComboBox()
            self.lvl_combo.addItems(['Level 1', 'Level 2', 'Level 3'])
            form.addRow("البرنامج:", self.prog_combo)
            form.addRow("المستوى:", self.lvl_combo)
            
        c_layout.addLayout(form)
        
        btn = QPushButton("تسجيل")
        btn.clicked.connect(self.register)
        c_layout.addWidget(btn)
        
        layout.addWidget(card)

    def register(self):
        name = self.name_inp.text()
        email = self.email_inp.text()
        
        if not name or not email:
            QMessageBox.warning(self, "خطأ", "البيانات ناقصة")
            return
            
        password = "123"
        
        try:
            if self.role == 'student':
                sid = str(random.randint(10000, 99999))
                prog = self.prog_combo.currentText()
                lvl = self.lvl_combo.currentText()
                
                if database.add_student(sid, name, email, prog, lvl):
                    db_handler.create_user_account(sid, email, password, 'student', name, self.mobile_inp.text())
                    QMessageBox.information(self, "تم", f"تم إنشاء الحساب.\nالمعرف: {sid}\nكلمة المرور: {password}")
                    self.accept()
                else:
                    QMessageBox.warning(self, "خطأ", "المعرف أو الايميل مستخدم مسبقاً")
            else:
                did = f"dr_{random.randint(100,999)}"
                db_handler.create_user_account(did, email, password, 'doctor', name, self.mobile_inp.text())
                QMessageBox.information(self, "تم", f"تم إنشاء الحساب.\nالمعرف: {did}\nكلمة المرور: {password}")
                self.accept()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ في قاعدة البيانات:\n{e}")

# --- نافذة الدخول ---
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تسجيل الدخول")
        self.resize(500, 400)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.user_data = None
        self.is_dark = False
        
        layout = QVBoxLayout(self)
        
        # Theme Toggle
        top = QHBoxLayout()
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setProperty("class", "theme_btn")
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.clicked.connect(self.toggle_theme)
        top.addWidget(self.theme_btn)
        top.addStretch()
        layout.addLayout(top)
        
        # Login Card
        card = QWidget(); card.setProperty("class", "card")
        apply_shadow(card)
        c_lay = QVBoxLayout(card)
        c_lay.setSpacing(15)
        
        c_lay.addWidget(QLabel("نظام التسجيل الجامعي ODUS"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.uid_inp = QLineEdit(); self.uid_inp.setPlaceholderText("المعرف الجامعي")
        self.pwd_inp = QLineEdit(); self.pwd_inp.setPlaceholderText("كلمة المرور")
        self.pwd_inp.setEchoMode(QLineEdit.EchoMode.Password)
        
        c_lay.addWidget(self.uid_inp)
        c_lay.addWidget(self.pwd_inp)
        
        btn_login = QPushButton("دخول")
        btn_login.clicked.connect(self.do_login)
        c_lay.addWidget(btn_login)
        
        h_lay = QHBoxLayout()
        btn_st = QPushButton("جديد (طالب)"); btn_st.setProperty("class", "secondary")
        btn_dr = QPushButton("جديد (دكتور)"); btn_dr.setProperty("class", "secondary")
        btn_st.clicked.connect(lambda: RegisterWindow('student', self).exec())
        btn_dr.clicked.connect(lambda: RegisterWindow('doctor', self).exec())
        h_lay.addWidget(btn_st); h_lay.addWidget(btn_dr)
        c_lay.addLayout(h_lay)
        
        layout.addWidget(card)
        
    def toggle_theme(self):
        app = QApplication.instance()
        self.is_dark = not self.is_dark
        if self.is_dark:
            app.setStyleSheet(DARK_MODE_QSS)
            self.theme_btn.setText("☀️")
        else:
            app.setStyleSheet(LIGHT_MODE_QSS)
            self.theme_btn.setText("🌙")
            
    def do_login(self):
        u = db_handler.db_login(self.uid_inp.text(), self.pwd_inp.text())
        if u:
            self.user_data = u
            self.accept()
        else:
            QMessageBox.warning(self, "خطأ", "بيانات الدخول غير صحيحة")

# --- لوحة الطالب ---
class StudentApp(QWidget):
    def __init__(self, user, is_dark=False):
        super().__init__()
        self.user = user
        self.is_dark = is_dark # حفظ حالة الثيم
        self.setWindowTitle(f"لوحة الطالب - {user['name']}")
        self.resize(1200, 700)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.registered_sched = []
        self.sec_group = QButtonGroup()
        
        self.init_ui()
        self.refresh_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Top Bar
        top = QHBoxLayout()
        
        # زر الثيم
        self.theme_btn = QPushButton("🌙" if not self.is_dark else "☀️")
        self.theme_btn.setProperty("class", "theme_btn")
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.clicked.connect(self.toggle_theme)
        top.addWidget(self.theme_btn)
        
        top.addWidget(QLabel(f"مرحباً، {self.user['name']} ({self.user['program']})"))
        top.addStretch()
        
        btn_exit = QPushButton("خروج"); btn_exit.setProperty("class", "danger")
        btn_exit.clicked.connect(self.close)
        top.addWidget(btn_exit)
        layout.addLayout(top)
        
        content = QHBoxLayout()
        
        # 1. Available Courses
        col1 = QFrame(); col1.setProperty("class", "card"); apply_shadow(col1)
        l1 = QVBoxLayout(col1)
        l1.addWidget(QLabel("1. اختر مادة"))
        self.course_list = QListWidget()
        self.course_list.currentItemChanged.connect(self.load_sections)
        l1.addWidget(self.course_list)
        content.addWidget(col1, 1)
        
        # 2. Sections
        col2 = QFrame(); col2.setProperty("class", "card"); apply_shadow(col2)
        l2 = QVBoxLayout(col2)
        self.sec_lbl = QLabel("2. اختر شعبة")
        l2.addWidget(self.sec_lbl)
        self.sec_table = QTableWidget(0, 5)
        self.sec_table.setHorizontalHeaderLabels(['', 'مدرس', 'وقت', 'قاعة', 'ID'])
        self.sec_table.setColumnHidden(4, True)
        l2.addWidget(self.sec_table)
        btn_add = QPushButton("تسجيل الشعبة"); btn_add.setProperty("class", "success")
        btn_add.clicked.connect(self.add_section)
        l2.addWidget(btn_add)
        content.addWidget(col2, 2)
        
        # 3. My Schedule
        col3 = QFrame(); col3.setProperty("class", "card"); apply_shadow(col3)
        l3 = QVBoxLayout(col3)
        l3.addWidget(QLabel("جدولي الدراسي"))
        self.my_table = QTableWidget(0, 5)
        self.my_table.setHorizontalHeaderLabels(['مادة', 'مدرس', 'وقت', 'ساعات', 'ID'])
        self.my_table.setColumnHidden(4, True)
        self.my_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        l3.addWidget(self.my_table)
        btn_del = QPushButton("حذف"); btn_del.setProperty("class", "danger")
        btn_del.clicked.connect(self.drop_section)
        l3.addWidget(btn_del)
        content.addWidget(col3, 2)
        
        layout.addLayout(content)

    def toggle_theme(self):
        app = QApplication.instance()
        self.is_dark = not self.is_dark
        if self.is_dark:
            app.setStyleSheet(DARK_MODE_QSS)
            self.theme_btn.setText("☀️")
        else:
            app.setStyleSheet(LIGHT_MODE_QSS)
            self.theme_btn.setText("🌙")
        
    def refresh_ui(self):
        db_handler.refresh_course_cache()
        self.registered_sched = database.get_student_schedule(self.user['id'])
        reg_ids = [r['course_code'] for r in self.registered_sched]
        
        self.course_list.clear()
        for code, data in db_handler.COURSE_CACHE.items():
            item = QListWidgetItem(f"{code}: {data['name']}")
            item.setData(Qt.ItemDataRole.UserRole, code)
            if code in reg_ids:
                item.setFlags(Qt.ItemFlag.NoItemFlags)
                item.setForeground(QColor("gray"))
            self.course_list.addItem(item)
            
        self.my_table.setRowCount(len(self.registered_sched))
        for r, row in enumerate(self.registered_sched):
            self.my_table.setItem(r, 0, QTableWidgetItem(row['course_name']))
            self.my_table.setItem(r, 1, QTableWidgetItem(row['instructor']))
            self.my_table.setItem(r, 2, QTableWidgetItem(f"{row['start']}-{row['end']}"))
            self.my_table.setItem(r, 3, QTableWidgetItem(str(row['credit_hours'])))
            self.my_table.setItem(r, 4, QTableWidgetItem(row['id']))

    def load_sections(self, item):
        if not item: return
        code = item.data(Qt.ItemDataRole.UserRole)
        cdata = db_handler.COURSE_CACHE.get(code)
        if not cdata: return
        
        self.sec_lbl.setText(f"شعب: {cdata['name']}")
        secs = cdata['sections']
        self.sec_table.setRowCount(len(secs))
        self.sec_group = QButtonGroup()
        
        for r, s in enumerate(secs):
            rb = QRadioButton()
            rb.setProperty("sid", s['id'])
            rb.setProperty("ccode", code)
            if s['current_enrollment'] >= s['max_capacity']:
                rb.setEnabled(False)
                rb.setText("ممتلئة")
            
            self.sec_group.addButton(rb)
            self.sec_table.setCellWidget(r, 0, rb)
            self.sec_table.setItem(r, 1, QTableWidgetItem(s['instructor']))
            self.sec_table.setItem(r, 2, QTableWidgetItem(f"{s['start']}-{s['end']}"))
            self.sec_table.setItem(r, 3, QTableWidgetItem(s['hall']))
            self.sec_table.setItem(r, 4, QTableWidgetItem(s['id']))

    def add_section(self):
        btn = self.sec_group.checkedButton()
        if not btn:
            QMessageBox.warning(self, "تنبيه", "اختر شعبة أولاً")
            return
        
        sid = btn.property("sid")
        ccode = btn.property("ccode")
        
        if database.register_student(self.user['id'], sid, ccode):
            QMessageBox.information(self, "نجاح", "تم التسجيل")
            self.sec_table.setRowCount(0)
            self.refresh_ui()
        else:
            QMessageBox.warning(self, "فشل", "لم يتم التسجيل (ربما مسجلة مسبقاً)")

    def drop_section(self):
        row = self.my_table.currentRow()
        if row == -1: return
        sid = self.my_table.item(row, 4).text()
        if database.unregister_student(self.user['id'], sid):
            self.refresh_ui()
            QMessageBox.information(self, "تم", "تم الحذف")

# --- لوحة رئيس القسم (HOD) ---
class HODDashboard(QWidget):
    def __init__(self, uid, is_dark=False):
        super().__init__()
        self.is_dark = is_dark
        self.setWindowTitle("لوحة رئيس القسم (HOD)")
        self.resize(1000, 700)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        self.init_ui()
        self.refresh_courses_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        h = QHBoxLayout()
        
        # زر الثيم
        self.theme_btn = QPushButton("🌙" if not self.is_dark else "☀️")
        self.theme_btn.setProperty("class", "theme_btn")
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.clicked.connect(self.toggle_theme)
        h.addWidget(self.theme_btn)
        
        h.addWidget(QLabel("إدارة النظام الأكاديمي"))
        h.addStretch()
        
        btn_out = QPushButton("خروج"); btn_out.setProperty("class", "danger")
        btn_out.clicked.connect(self.close)
        h.addWidget(btn_out)
        layout.addLayout(h)
        
        self.tabs = QTabWidget()
        
        # Tab 1: Courses
        self.tab_courses = QWidget()
        self.setup_course_tab()
        self.tabs.addTab(self.tab_courses, "المواد")
        
        # Tab 2: Sections
        self.tab_sections = QWidget()
        self.setup_section_tab()
        self.tabs.addTab(self.tab_sections, "الشعب")
        
        layout.addWidget(self.tabs)

    def toggle_theme(self):
        app = QApplication.instance()
        self.is_dark = not self.is_dark
        if self.is_dark:
            app.setStyleSheet(DARK_MODE_QSS)
            self.theme_btn.setText("☀️")
        else:
            app.setStyleSheet(LIGHT_MODE_QSS)
            self.theme_btn.setText("🌙")

    def setup_course_tab(self):
        lay = QHBoxLayout(self.tab_courses)
        
        # List
        frame_list = QFrame(); frame_list.setProperty("class", "card")
        l = QVBoxLayout(frame_list)
        l.addWidget(QLabel("قائمة المواد"))
        self.course_list = QListWidget()
        l.addWidget(self.course_list)
        btn_del = QPushButton("حذف المادة"); btn_del.setProperty("class", "danger")
        btn_del.clicked.connect(self.del_course)
        l.addWidget(btn_del)
        lay.addWidget(frame_list)
        
        # Form
        frame_form = QFrame(); frame_form.setProperty("class", "card")
        f = QVBoxLayout(frame_form)
        f.addWidget(QLabel("إضافة مادة جديدة"))
        form = QFormLayout()
        self.c_code = QLineEdit()
        self.c_name = QLineEdit()
        self.c_cred = QLineEdit()
        form.addRow("الرمز:", self.c_code)
        form.addRow("الاسم:", self.c_name)
        form.addRow("الساعات:", self.c_cred)
        f.addLayout(form)
        btn_save = QPushButton("حفظ"); btn_save.setProperty("class", "success")
        btn_save.clicked.connect(self.add_course)
        f.addWidget(btn_save)
        f.addStretch()
        lay.addWidget(frame_form)

    def setup_section_tab(self):
        lay = QVBoxLayout(self.tab_sections)
        
        # Filter
        top = QHBoxLayout()
        top.addWidget(QLabel("اختر مادة:"))
        self.combo_courses = QComboBox()
        self.combo_courses.currentIndexChanged.connect(self.load_sections_table)
        top.addWidget(self.combo_courses)
        lay.addLayout(top)
        
        # Table
        self.sec_table = QTableWidget(0, 6)
        self.sec_table.setHorizontalHeaderLabels(['ID', 'مدرس', 'من', 'إلى', 'قاعة', 'سعة'])
        self.sec_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        lay.addWidget(self.sec_table)
        
        # Add Section Inputs
        bot = QHBoxLayout()
        self.ns_id = QLineEdit(); self.ns_id.setPlaceholderText("ID (e.g. 101)")
        self.ns_inst = QLineEdit(); self.ns_inst.setPlaceholderText("Dr. Name")
        self.ns_st = QLineEdit(); self.ns_st.setPlaceholderText("Start (8-16)")
        self.ns_en = QLineEdit(); self.ns_en.setPlaceholderText("End")
        self.ns_hall = QLineEdit(); self.ns_hall.setPlaceholderText("Hall")
        self.ns_cap = QLineEdit(); self.ns_cap.setPlaceholderText("Cap")
        
        for w in [self.ns_id, self.ns_inst, self.ns_st, self.ns_en, self.ns_hall, self.ns_cap]:
            bot.addWidget(w)
            
        btn_add = QPushButton("إضافة"); btn_add.clicked.connect(self.add_section)
        bot.addWidget(btn_add)
        lay.addLayout(bot)

    def refresh_courses_ui(self):
        db_handler.refresh_course_cache()
        self.course_list.clear()
        
        if hasattr(self, 'combo_courses'):
            self.combo_courses.clear()
            
        for code, data in db_handler.COURSE_CACHE.items():
            self.course_list.addItem(f"{code}: {data['name']}")
            if hasattr(self, 'combo_courses'):
                self.combo_courses.addItem(code)

    def add_course(self):
        code = self.c_code.text().strip().upper()
        name = self.c_name.text().strip()
        try:
            cred = int(self.c_cred.text())
            if not code or not name: raise ValueError
            
            database.upsert_course(code, name, cred, [])
            QMessageBox.information(self, "تم", "تمت إضافة المادة")
            self.refresh_courses_ui()
        except:
            QMessageBox.warning(self, "خطأ", "تأكد من إدخال البيانات صحيحة (الساعات رقم)")

    def del_course(self):
        itm = self.course_list.currentItem()
        if itm:
            code = itm.text().split(':')[0]
            database.delete_course(code)
            self.refresh_courses_ui()

    def load_sections_table(self):
        code = self.combo_courses.currentText()
        if not code: return
        
        data = db_handler.COURSE_CACHE.get(code)
        if not data: return
        
        secs = data['sections']
        self.sec_table.setRowCount(len(secs))
        for r, s in enumerate(secs):
            self.sec_table.setItem(r, 0, QTableWidgetItem(s['id']))
            self.sec_table.setItem(r, 1, QTableWidgetItem(s['instructor']))
            self.sec_table.setItem(r, 2, QTableWidgetItem(str(s['start'])))
            self.sec_table.setItem(r, 3, QTableWidgetItem(str(s['end'])))
            self.sec_table.setItem(r, 4, QTableWidgetItem(s['hall']))
            self.sec_table.setItem(r, 5, QTableWidgetItem(str(s['max_capacity'])))

    def add_section(self):
        cur_course = self.combo_courses.currentText()
        if not cur_course:
            QMessageBox.warning(self, "تنبيه", "يجب إضافة مواد أولاً واختيار مادة من القائمة!")
            return
            
        try:
            d = {
                'id': self.ns_id.text(),
                'course_code': cur_course,
                'instructor': self.ns_inst.text(),
                'start': int(self.ns_st.text()),
                'end': int(self.ns_en.text()),
                'hall': self.ns_hall.text(),
                'max_capacity': int(self.ns_cap.text())
            }
            database.upsert_section(d)
            db_handler.refresh_course_cache()
            self.load_sections_table()
            QMessageBox.information(self, "تم", "تمت الإضافة")
        except ValueError:
            QMessageBox.warning(self, "خطأ", "الوقت والسعة يجب أن تكون أرقاماً")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))

# --- التشغيل ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(LIGHT_MODE_QSS)
    
    try:
        db_handler.create_user_account("admin", "admin@uni.edu", "admin", "hod", "Admin", "000")
    except: pass
    
    while True:
        win = LoginWindow()
        if win.exec() == QDialog.DialogCode.Accepted:
            role = win.user_data['role']
            is_dark_mode = win.is_dark # حفظ حالة الثيم المختارة
            
            if role == 'student':
                main = StudentApp(win.user_data, is_dark=is_dark_mode)
            elif role == 'hod' or role == 'admin':
                main = HODDashboard(win.user_data['id'], is_dark=is_dark_mode)
            else:
                main = QLabel("Doctor Dashboard (Under Construction)")
                main.resize(400,200)
                
            # تطبيق الثيم المختار قبل العرض
            if is_dark_mode:
                app.setStyleSheet(DARK_MODE_QSS)
            else:
                app.setStyleSheet(LIGHT_MODE_QSS)
            
            main.show()
            app.exec()
            break
        else:
            break
            
    sys.exit()