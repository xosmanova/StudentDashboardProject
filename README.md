# Mini Project: Student Performance Dashboard 🎓

Bu layihə **Streamlit** və **Microsoft SQL Server (MSSQL)** istifadə edərək tələbə nəticələrinin idarə edilməsi, statistik təhlili və dinamik dərəcələndirilməsi (Grade) üçün hazırlanmış tam web tətbiqidir.

Layihə **Clean Code** prinsiplərinə və **Mərhələli Memarlıq (Layered Architecture)** standartlarına tam uyğundur:

```
SQL Server (UniversityDB)
        ↓
Database Layer (database.py)
        ↓
Business Logic (services.py)
        ↓
Streamlit UI (app.py)
```

---

## 📁 Fayl Strukturu

```
MiniProjectStudent/
│
├── config.py                 # Konfiqurasiya sabitlər (No Magic Numbers)
├── database.py               # Database layer (create_connection, add_student, get_students, get_student)
├── services.py               # Business logic layer (calculate_grade, calculate_statistics, validations)
├── app.py                    # Streamlit UI təqdimat qatı
├── requirements.txt          # Asılılıqlar (streamlit, pyodbc, pandas)
├── task1_university_db.sql   # Task 1: SQL Server Database & GetStudentResult Stored Procedure
├── task2_refactoring.py      # Task 2: Pis kod vs Clean Code müqayisəli icra faylı
├── task2_refactoring_guide.md# Task 2: Refactoring haqqında ətraflı izahat sənədi
├── test_services.py          # Biznes məntiqi üçün Unit testlər
└── README.md                 # Layihə sənədləşdirməsi
```

---

## 🎯 Təhvil Verilən 3 Əsas Tapşırıq (Deliverables)

### 📌 Task 1 — SQL Server
* **Database:** `UniversityDB`
* **Table:** `Students` (`Id`, `Name`, `Score`, `CreatedAt`)
* **Stored Procedure:** `GetStudentResult`
  * Parametrsiz çağırıldıqda: bütün tələbələri bala görə sıralanmış qaytarır (`EXEC GetStudentResult;`).
  * Parametr ilə çağırıldıqda: tələbə adına görə filtrasiya edir (`EXEC GetStudentResult @StudentName = 'Ali';`).
* **Köməkçi Stored Procedure:** `AddStudent`
* **Skript faylı:** [task1_university_db.sql](file:///c:/Users/Lenovo/OneDrive/Desktop/5094a2-proglanguage/MiniProjectStudent/task1_university_db.sql)

### 📌 Task 2 — Python (Clean Code Refactoring)
* **Problem:** Bir funksiyada hər şeyi edən spagetti kod, tək hərfli mənasız dəyişənlər (`d`, `s`, `m`, `t`), `90`, `80`, `70`, `60`, `999` kimi **Magic Numbers**, SRP və DRY pozuntuları.
* **Həll:**
  1. **Meaningful Names:** Məqsədyönlü adlar (`student_name`, `student_score`, `total_students`, `average_score`).
  2. **No Magic Numbers:** Sabitlərin təyini (`EXCELLENT_GRADE_MIN_SCORE = 90.0`, `PASSING_GRADE_MIN_SCORE = 60.0`).
  3. **Single Responsibility (SRP):** Tək məqsədli kiçik funksiyalar: `is_valid_score()`, `calculate_grade()`, `calculate_statistics()`, `process_student_results()`.
  4. **DRY & KISS:** Sadə, anlaşılan və təkrar olunmayan struktur.
  5. **Type hints & Docstrings:** Funksiya giriş və çıxış tiplərinin dəqiq qeyd olunması.
* **Fayllar:** [task2_refactoring.py](file:///c:/Users/Lenovo/OneDrive/Desktop/5094a2-proglanguage/MiniProjectStudent/task2_refactoring.py) və [task2_refactoring_guide.md](file:///c:/Users/Lenovo/OneDrive/Desktop/5094a2-proglanguage/MiniProjectStudent/task2_refactoring_guide.md)

### 📌 Task 3 — Streamlit Web Tətbiqi
* **1. Student əlavə etmək:**
  * Form: `Student Name`, `Score` (0-100), `[Add Student]` düyməsi.
  * Məlumatların daxil edilməsi dərhal `UniversityDB`-yə yazılır və ekran yenilənir.
* **2. Student siyahısını göstərmək:**
  * `Name`, `Score`, `Grade` sütunları ilə səliqəli cədvəl (`st.dataframe`).
  * Grade dərəcələri biznes məntiqində dinamik hesablanır:
    * 90 – 100 $\rightarrow$ **A**
    * 80 – 89.9 $\rightarrow$ **B**
    * 70 – 79.9 $\rightarrow$ **C**
    * 60 – 69.9 $\rightarrow$ **D**
    * < 60 $\rightarrow$ **F**
* **3. Student axtarışı:**
  * `Search Student` axtarış inputu (`st.text_input`). SQL Server Stored Procedure-u vasitəsilə axtarış aparılır.
* **4. Statistikalar (KPI Kartları):**
  * `Total Students`
  * `Average Score`
  * `Highest Score`
  * `Lowest Score`
* **5. Vizual Qrafik:**
  * Tələbə ballarının interaktiv vizual bar chart-ı.

---

## 🚀 Quraşdırma və İşə Salma Təlimatı

### 1. Kitabxanaları quraşdırın:
```bash
pip install -r requirements.txt
```

### 2. SQL Server Bazasını qurun:
SQL Server Management Studio (SSMS) və ya `sqlcmd` ilə:
```bash
sqlcmd -S ".\SQLEXPRESS" -E -i "task1_university_db.sql"
```

### 3. Task 2 Refactoring kodunu icra edin:
```bash
python task2_refactoring.py
```

### 4. Unit Testləri yoxlayın:
```bash
python -m unittest test_services.py
```

### 5. Streamlit Tətbiqini işə salın:
```bash
streamlit run app.py
```
Tətbiq brauzerinizdə `http://localhost:8501` ünvanında açılacaqdır.

---

## 🌐 Streamlit Community Cloud-da Canlı Deploy (Müəllimə Təqdimat Üçün)

Layihə buludda sıfır konfiqurasiya ilə deploy oluna bilməsi üçün xüsusi olaraq hazırlanmışdır (**Dual-Mode Database Architecture**):

1. **GitHub Reposuna Push edin:**
   ```bash
   git add .
   git commit -m "Configure cloud deployment support"
   git push origin master
   ```

2. **Streamlit Cloud Hesabına Daxil Olun:**
   - [share.streamlit.io](https://share.streamlit.io) saytına daxil olun.
   - **Continue with GitHub** seçin.

3. **Yeni Tətbiq (New App) Yaradın:**
   - **Repository:** `xosmanova/StudentDashboardProject`
   - **Branch:** `master`
   - **Main file path:** `app.py`
   - **Deploy!** düyməsinə klikləyin.

4. 1-2 dəqiqə ərzində saytınız bütün dünyada əlçatan olan pulsuz domen linki alacaq (məsələn: `https://studentdashboardproject.streamlit.app`) və həmin linki birbaşa müəlliminizə təqdim edə bilərsiniz!
