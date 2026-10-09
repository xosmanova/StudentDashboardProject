# Task 2: Python — Pis Yazılmış Kodun Clean Code Prinsiplərinə Uyğun Refactoring-i

Bu sənəd tələbə nəticələrinin idarə edilməsi və dərəcələndirilməsi üzrə **pis yazılmış (spaghetti / bad code)** Python kodunun **Clean Code** prinsiplərinə uyğun olaraq addım-addım necə refactor edildiyini nümayiş etdirir.

---

## 1. Pis Yazılmış Kod (Before Refactoring)

```python
def do_everything(d):
    t = 0
    m = -1
    mn = 999
    res = []
    for item in d:
        n = item[0]
        s = item[1]
        if s > 100 or s < 0:
            print("xeta!")
            continue
        t += s
        if s > m:
            m = s
        if s < mn:
            mn = s
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
```

### Kodun Əsas Qüsurları:
1. **Meaningful Names Qaydası Pozulub:**
   - Dəyişən adları (`d`, `t`, `m`, `mn`, `n`, `s`, `g`, `res`) tək hərflidir və onların nəyi təmsil etdiyi heç kimə aydın deyil.
2. **Single Responsibility Principle (SRP) Pozulub:**
   - `do_everything` adlı bir nəhəng funksiya eyni zamanda məlumatları parse edir, validasiya aparır, dərəcə (Grade) hesablayır, orta bal tapır, minimum/maksimum müəyyən edir və nəticələri ekrana çap edir.
3. **Magic Numbers İstifadə Edilib:**
   - Kod daxilində birbaşa `100`, `0`, `999`, `90`, `80`, `70`, `60` rəqəmləri qeyd olunub. Bu rəqəmlərin nəyi ifadə etdiyi və dəyişdirilməsi lazım olduqda harada dəyişdiriləcəyi qeyri-müəyyəndir.
4. **DRY (Don't Repeat Yourself) Pozulub:**
   - Məlumatların dərəcələndirilməsi və yoxlanışı digər yerlərdə təkrar istifadə edilə bilmir.
5. **KISS (Keep It Simple, Stupid) Pozulub:**
   - `len(d) > 0` təkrar yoxlamaları və spagetti `for` dövrü kodu qəlizləşdirir.
6. **Error Handling & Type Hinting Yoxdur:**
   - Tiplər qeyd olunmayıb, xətalar yalnız `print("xeta!")` ilə səssiz ötürülür.

---

## 2. Clean Code Qaydalarının Tətbiqi (Refactoring Addımları)

### Qayda 1: Meaningful Names (Mənalı Adlar)
- `d` $\rightarrow$ `student_records`
- `n` $\rightarrow$ `student_name`
- `s` $\rightarrow$ `student_score`
- `t` $\rightarrow$ `total_score`
- `g` $\rightarrow$ `letter_grade`
- `do_everything()` $\rightarrow$ Ayrı-ayrı məqsədyönlü funksiyalar: `calculate_grade()`, `calculate_statistics()`.

### Qayda 2: Magic Numbers Aradan Qaldırılması (Sabitlər)
Bütün rəqəmlər mənalı adlara malik sabitlərə (`Final`) çevrildi:
```python
EXCELLENT_GRADE_MIN_SCORE: Final[float] = 90.0
GOOD_GRADE_MIN_SCORE: Final[float] = 80.0
SATISFACTORY_GRADE_MIN_SCORE: Final[float] = 70.0
PASSING_GRADE_MIN_SCORE: Final[float] = 60.0

MINIMUM_VALID_SCORE: Final[float] = 0.0
MAXIMUM_VALID_SCORE: Final[float] = 100.0
```

### Qayda 3: Single Responsibility Principle (SRP)
Hər funksiya yalnız bir işə cavabdehdir:
1. `is_valid_score(score)` — Yalnız balın düzgünlüyünü yoxlayır.
2. `calculate_grade(student_score)` — Yalnız balın hərf qarşılığını (A, B, C, D, F) hesablayır.
3. `calculate_statistics(records)` — Yalnız statistik göstəriciləri (Total, Average, Max, Min) hesablayır.
4. `print_summary_report(...)` — Yalnız konsola formatlaşdırılmış nəticələri çıxarır (UI/Console qatı).

### Qayda 4: DRY & KISS
- Grade hesablama və statistika məntiqi tam izolyasiya olunub və istənilən yerdən təkrar istifadə edilə bilər.
- Funksiyalar sadə, oxunaqlı və qısa saxlanılıb (10-15 sətirdən az).

---

## 3. Refactoring Olunmuş Təmiz Kod (After Refactoring)

```python
from typing import Any, Final

# 1. Sabitlər (No Magic Numbers)
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


def is_valid_score(score: float) -> bool:
    """Yalnız balın 0 ilə 100 arasında olmasını yoxlayır."""
    return MINIMUM_VALID_SCORE <= score <= MAXIMUM_VALID_SCORE


def calculate_grade(student_score: float) -> str:
    """Tələbə balına əsasən hərf qiymətini (Grade) müəyyən edir."""
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
    """Tələbə siyahısından statistik göstəriciləri hesablayır."""
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
```

---

## 4. Xülasə: Before vs After Müqayisə Cədvəli

| Göstərici | Əvvəl (Pis Kod) | Sonra (Clean Code) |
| :--- | :--- | :--- |
| **Dəyişən adları** | `d`, `t`, `m`, `mn`, `s` | `student_score`, `total_students`, `average_score` |
| **Magic Numbers** | `90`, `80`, `70`, `60`, `999` kodun içində | `EXCELLENT_GRADE_MIN_SCORE = 90.0` və s. sabitləri |
| **Funksiyanın rolu** | Hər şeyi edən spagetti funksiya | Tək məqsədli kiçik funksiyalar (SRP) |
| **Təkrar istifadə** | Qeyri-mümkündür | Asanlıqla import və təkrar istifadə oluna bilər (DRY) |
| **Tip təhlükəsizliyi**| Yoxdur | Type hints (`float`, `list[dict]`, `str`) |
| **Oxunaqlılıq** | Çox çətin və qaranlıq | Özü-özünü izah edən (Self-documenting) kod |
