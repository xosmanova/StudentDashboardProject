"""
services.py
Business logic layer for the Student Performance Dashboard.
Handles grade calculations, statistical aggregations, and input validation.
Follows Clean Code principles: Single Responsibility, DRY, KISS, and meaningful names.
"""

from typing import Any
from config import (
    GRADE_A_MIN_SCORE,
    GRADE_B_MIN_SCORE,
    GRADE_C_MIN_SCORE,
    GRADE_D_MIN_SCORE,
    GRADE_LETTER_A,
    GRADE_LETTER_B,
    GRADE_LETTER_C,
    GRADE_LETTER_D,
    GRADE_LETTER_F,
    MAX_VALID_SCORE,
    MIN_VALID_SCORE,
)


def calculate_grade(score: float) -> str:
    """
    Determines the letter grade corresponding to a numeric score.
    Uses centralized constants to avoid magic numbers.
    
    Grading Scale:
        90 - 100 : A
        80 - 89.9: B
        70 - 79.9: C
        60 - 69.9: D
        Below 60 : F
        
    Args:
        score (float): The numerical score achieved by the student (0 to 100).
        
    Returns:
        str: Corresponding letter grade ('A', 'B', 'C', 'D', 'F').
        
    Raises:
        ValueError: If score is outside the valid range [0, 100].
    """
    if score < MIN_VALID_SCORE or score > MAX_VALID_SCORE:
        raise ValueError(
            f"Score must be between {MIN_VALID_SCORE} and {MAX_VALID_SCORE}. Provided: {score}"
        )

    if score >= GRADE_A_MIN_SCORE:
        return GRADE_LETTER_A
    if score >= GRADE_B_MIN_SCORE:
        return GRADE_LETTER_B
    if score >= GRADE_C_MIN_SCORE:
        return GRADE_LETTER_C
    if score >= GRADE_D_MIN_SCORE:
        return GRADE_LETTER_D

    return GRADE_LETTER_F


def calculate_statistics(students: list[dict[str, Any]]) -> dict[str, float | int]:
    """
    Computes key performance indicators from a list of student records.
    
    Required Metrics:
        - Total Students
        - Average Score
        - Highest Score
        - Lowest Score
        
    Args:
        students (list[dict[str, Any]]): List of student records, each having a 'Score' field.
        
    Returns:
        dict[str, float | int]: Dictionary containing aggregated statistical values.
    """
    if not students:
        return {
            "total_students": 0,
            "average_score": 0.0,
            "highest_score": 0.0,
            "lowest_score": 0.0,
        }

    scores = [float(student["Score"]) for student in students]
    total_students = len(scores)
    average_score = round(sum(scores) / total_students, 1)
    highest_score = round(max(scores), 1)
    lowest_score = round(min(scores), 1)

    return {
        "total_students": total_students,
        "average_score": average_score,
        "highest_score": highest_score,
        "lowest_score": lowest_score,
    }


def validate_student_input(name: str, score: float) -> tuple[bool, str]:
    """
    Validates form input before writing to the database.
    
    Args:
        name (str): Student name input.
        score (float): Numeric score.
        
    Returns:
        tuple[bool, str]: (is_valid, validation_error_message)
    """
    cleaned_name = name.strip() if name else ""
    if not cleaned_name:
        return False, "Student Name cannot be empty."

    if len(cleaned_name) < 2:
        return False, "Student Name must have at least 2 characters."

    if score < MIN_VALID_SCORE or score > MAX_VALID_SCORE:
        return False, f"Score must be between {MIN_VALID_SCORE} and {MAX_VALID_SCORE}."

    return True, ""


def enrich_students_with_grade(students: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Enhances raw database student records by appending the calculated letter grade.
    Returns a new list of dictionaries without mutating original inputs (immutability best practice).
    
    Args:
        students (list[dict[str, Any]]): Raw student records from the database.
        
    Returns:
        list[dict[str, Any]]: Student records including the 'Grade' attribute.
    """
    enriched: list[dict[str, Any]] = []
    for student in students:
        score_val = float(student.get("Score", 0.0))
        grade_val = calculate_grade(score_val)
        enriched.append({
            "Id": student.get("Id"),
            "Name": student.get("Name"),
            "Score": score_val,
            "Grade": grade_val,
        })
    return enriched
