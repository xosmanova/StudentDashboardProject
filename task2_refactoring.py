"""
task2_refactoring.py
=============================================================================
TASK 2: PİS YAZILMIŞ KODUN CLEAN CODE PRİNSİPLƏRİNƏ UYĞUN REFACTORING-İ
=============================================================================
Bu fayl iki hissədən ibarətdir:
1. BEFORE: Clean Code qaydalarını pozan "Pis Kod" nümunəsi
2. AFTER : Clean Code prinsiplərinə uyğun yenidən yazılmış (Refactored) "Təmiz Kod"

Qaydalar:
1. Meaningful Names
2. Single Responsibility (SRP)
3. DRY (Don't Repeat Yourself)
4. KISS (Keep It Simple, Stupid)
5. Magic Numbers (Sabitlərin təyini)
6. Funksiyaların ölçüsü (Kiçik və aydın funksiyalar)
"""

import sys
from typing import Any, Final

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# =============================================================================
# HİSSƏ 1: PİS YAZILMIŞ KOD (BEFORE REFACTORING)
# =============================================================================
# Çatışmazlıqlar:
# - Mənasız adlandırma: x, d, s, fn, l
# - Magic Numbers: 90, 80, 70, 60, 0, 100 birbaşa kodun içindədir
# - SRP pozulması: tək bir böyük funksiya həm hesablama, həm validasiya, həm print edir
# - DRY pozulması: dərəcə hesablama məntiqi təkrar yazılır
# - Tip annotasiyası və docstring yoxdur
# -----------------------------------------------------------------------------

def do_everything(d):
    # Pis kod: nə etdiyi aydın olmayan dəyişənlər və spagetti məntiq
    t = 0
    m = -1
    mn = 999
    res = []
    
    for item in d:
        n = item[0]
        s = item[1]
        
        # Magic numbers və qeyri-dəqiq yoxlama
        if s > 100 or s < 0:
            print("xeta!")
            continue
            
        t += s
        if s > m:
            m = s
        if s < mn:
            mn = s
            
        # Magic numbers və təkrar kod
        g = "F"
        if s >= 90:
            g = "A"
        elif s >= 80:
            g = "B"
        elif s >= 70:
            g = "C"
        elif s >= 60:
            g = "D"
            
        res.append((n, s, g))
        print(n + " bal: " + str(s) + " derecesi: " + g)
        
    avg = t / len(d) if len(d) > 0 else 0
    print("Orta: " + str(avg))
    print("Max: " + str(m))
    print("Min: " + str(mn))
    return res


# =============================================================================
# HİSSƏ 2: CLEAN CODE İLƏ REFACTORING OLUNMUŞ KOD (AFTER REFACTORING)
# =============================================================================

# 1. Magic Numbers aradan qaldırıldı (Sabitlər)
EXCELLENT_GRADE_MIN_SCORE: Final[float] = 90.0
GOOD_GRADE_MIN_SCORE: Final[float] = 80.0
SATISFACTORY_GRADE_MIN_SCORE: Final[float] = 70.0
PASSING_GRADE_MIN_SCORE: Final[float] = 60.0

MINIMUM_VALID_SCORE: Final[float] = 0.0
MAXIMUM_VALID_SCORE: Final[float] = 100.0

GRADE_A: Final[str] = "A"
GRADE_B: Final[str] = "B"
GRADE_C: Final[str] = "C"
GRADE_D: Final[str] = "D"
GRADE_F: Final[str] = "F"


# 2. Kiçik funksiyalar və Single Responsibility (SRP)

def is_valid_score(score: float) -> bool:
    """Yalnız balın 0 ilə 100 arasında olmasını yoxlayır (Tək Məsuliyyət)."""
    return MINIMUM_VALID_SCORE <= score <= MAXIMUM_VALID_SCORE


def calculate_grade(student_score: float) -> str:
    """
    Tələbə balına əsasən hərf qiymətini (Grade) müəyyən edir.
    Meaningful names və sabitlərdən istifadə edir (No Magic Numbers).
    """
    if not is_valid_score(student_score):
        raise ValueError(
            f"Bal {MINIMUM_VALID_SCORE} və {MAXIMUM_VALID_SCORE} aralığında olmalıdır. Daxil edilən: {student_score}"
        )

    if student_score >= EXCELLENT_GRADE_MIN_SCORE:
        return GRADE_A
    if student_score >= GOOD_GRADE_MIN_SCORE:
        return GRADE_B
    if student_score >= SATISFACTORY_GRADE_MIN_SCORE:
        return GRADE_C
    if student_score >= PASSING_GRADE_MIN_SCORE:
        return GRADE_D

    return GRADE_F


def calculate_statistics(student_records: list[dict[str, Any]]) -> dict[str, float | int]:
    """
    Tələbə siyahısından statistikanı hesablayır (Tək Məsuliyyət).
    """
    if not student_records:
        return {
            "total_students": 0,
            "average_score": 0.0,
            "highest_score": 0.0,
            "lowest_score": 0.0,
        }

    scores = [record["score"] for record in student_records]
    total_count = len(scores)

    return {
        "total_students": total_count,
        "average_score": round(sum(scores) / total_count, 1),
        "highest_score": round(max(scores), 1),
        "lowest_score": round(min(scores), 1),
    }


def process_student_results(raw_data: list[tuple[str, float]]) -> list[dict[str, Any]]:
    """
    Xam məlumatları təmizləyir, dərəcələndirir və strukturlu siyahı halına gətirir (KISS).
    """
    processed_results: list[dict[str, Any]] = []

    for name, score in raw_data:
        if not is_valid_score(score):
            continue

        grade = calculate_grade(score)
        processed_results.append({
            "name": name,
            "score": score,
            "grade": grade,
        })

    return processed_results


def print_summary_report(students: list[dict[str, Any]], stats: dict[str, float | int]) -> None:
    """Hesabatın konsola səliqəli çıxarılması (Tək Məsuliyyət - I/O presentation)."""
    print("-" * 35)
    print(f"{'Name':<12} {'Score':<10} {'Grade':<5}")
    print("-" * 35)
    for student in students:
        print(f"{student['name']:<12} {student['score']:<10} {student['grade']:<5}")
    print("-" * 35)
    print(f"Total Students : {stats['total_students']}")
    print(f"Average Score  : {stats['average_score']}")
    print(f"Highest Score  : {stats['highest_score']}")
    print(f"Lowest Score   : {stats['lowest_score']}")
    print("-" * 35)


# =============================================================================
# DEMO İCRA VƏ MÜQAYİSƏ
# =============================================================================
if __name__ == "__main__":
    sample_students = [
        ("Ali", 85.0),
        ("Leyla", 72.0),
        ("Murad", 48.0),
        ("Aysel", 91.0),
        ("Kamran", 63.0),
    ]

    print("\n>>> [1] PİS YAZILMIŞ KODUN NƏTİCƏSİ:")
    do_everything(sample_students)

    print("\n>>> [2] CLEAN CODE İLƏ REFACTORING OLUNMUŞ KODUN NƏTİCƏSİ:")
    clean_results = process_student_results(sample_students)
    clean_stats = calculate_statistics(clean_results)
    print_summary_report(clean_results, clean_stats)
