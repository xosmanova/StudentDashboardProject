"""
config.py
Configuration settings and constants for the Student Performance Dashboard.
Follows Clean Code principles by eliminating magic numbers and centralizing application configurations.
"""

from typing import Final

# ==============================================================================
# Database Configuration
# ==============================================================================
DEFAULT_DB_SERVER: Final[str] = r".\SQLEXPRESS"
DEFAULT_DB_NAME: Final[str] = "UniversityDB"
DEFAULT_ODBC_DRIVER: Final[str] = "ODBC Driver 17 for SQL Server"

# Supported drivers in order of preference
PREFERRED_DRIVERS: Final[list[str]] = [
    "ODBC Driver 17 for SQL Server",
    "ODBC Driver 18 for SQL Server",
    "SQL Server",
]

# ==============================================================================
# Business Logic / Grade Calculation Constants (No Magic Numbers)
# ==============================================================================
GRADE_A_MIN_SCORE: Final[float] = 90.0
GRADE_B_MIN_SCORE: Final[float] = 80.0
GRADE_C_MIN_SCORE: Final[float] = 70.0
GRADE_D_MIN_SCORE: Final[float] = 60.0

MIN_VALID_SCORE: Final[float] = 0.0
MAX_VALID_SCORE: Final[float] = 100.0

GRADE_LETTER_A: Final[str] = "A"
GRADE_LETTER_B: Final[str] = "B"
GRADE_LETTER_C: Final[str] = "C"
GRADE_LETTER_D: Final[str] = "D"
GRADE_LETTER_F: Final[str] = "F"

# ==============================================================================
# UI & Dashboard Display Constants
# ==============================================================================
APP_TITLE: Final[str] = "Student Performance Dashboard"
APP_ICON: Final[str] = "🎓"
APP_SUBTITLE: Final[str] = "Tələbə Nəticələrinin İdarə Edilməsi və Analitikası"
