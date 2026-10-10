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

