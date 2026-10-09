"""
database.py
Database access layer for the Student Performance Dashboard.
Handles connections and database operations for UniversityDB on SQL Server.
Follows Clean Code principles: Single Responsibility, DRY, and secure parameterized queries.
"""

import logging
from typing import Any, Optional
import pyodbc

from config import (
    DEFAULT_DB_NAME,
    DEFAULT_DB_SERVER,
    DEFAULT_ODBC_DRIVER,
    PREFERRED_DRIVERS,
)

logger = logging.getLogger(__name__)


def _detect_installed_driver() -> str:
    """
    Detects the best available SQL Server ODBC driver on the host system.
    Falls back to default driver if detection yields no preferred match.
    """
    try:
        available_drivers = pyodbc.drivers()
        for driver in PREFERRED_DRIVERS:
            if driver in available_drivers:
                return driver
    except Exception as exc:
        logger.warning("Could not enumerate ODBC drivers: %s", exc)

    return DEFAULT_ODBC_DRIVER


def build_connection_string(
    server: str = DEFAULT_DB_SERVER,
    database: str = DEFAULT_DB_NAME,
    driver: Optional[str] = None,
) -> str:
    """
    Constructs a secure ODBC connection string using Windows Trusted Authentication.
    """
    selected_driver = driver or _detect_installed_driver()
    
    # TrustServerCertificate is recommended for Driver 18+ to avoid local SSL validation errors
    extra_params = ""
    if "18" in selected_driver:
        extra_params = ";TrustServerCertificate=yes"

    return (
        f"DRIVER={{{selected_driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
        f"{extra_params}"
    )


def create_connection(
    server: str = DEFAULT_DB_SERVER,
    database: str = DEFAULT_DB_NAME,
) -> pyodbc.Connection:
    """
    Establishes and returns an active connection to the SQL Server database.
    
    Raises:
        pyodbc.Error: If connection cannot be established.
    """
    connection_string = build_connection_string(server=server, database=database)
    return pyodbc.connect(connection_string, autocommit=True)


def _row_to_dict(cursor: pyodbc.Cursor, row: pyodbc.Row) -> dict[str, Any]:
    """
    Helper function to map a pyodbc Row to a Python dictionary using column names.
    Adheres to DRY principle across query functions.
    """
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))


def get_students() -> list[dict[str, Any]]:
    """
    Retrieves all students from UniversityDB using the GetStudentResult stored procedure.
    
    Returns:
        list[dict[str, Any]]: List of student dictionaries with keys like 'Id', 'Name', 'Score'.
    """
    students: list[dict[str, Any]] = []
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Call Stored Procedure GetStudentResult without filter
            cursor.execute("EXEC dbo.GetStudentResult;")
            rows = cursor.fetchall()
            for row in rows:
                students.append(_row_to_dict(cursor, row))
    finally:
        connection.close()

    return students


def get_student(name: str) -> list[dict[str, Any]]:
    """
    Searches and retrieves students whose names match the query string.
    Calls the GetStudentResult stored procedure with @StudentName parameter.
    
    Args:
        name (str): The search keyword or student name.
        
    Returns:
        list[dict[str, Any]]: Matching student records.
    """
    students: list[dict[str, Any]] = []
    cleaned_name = name.strip() if name else ""

    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC dbo.GetStudentResult @StudentName = ?", (cleaned_name,))
            rows = cursor.fetchall()
            for row in rows:
                students.append(_row_to_dict(cursor, row))
    finally:
        connection.close()

    return students


def add_student(name: str, score: float) -> bool:
    """
    Inserts a new student record into the Students table.
    Uses parameterized query to prevent SQL Injection and ensure data safety.
    
    Args:
        name (str): Name of the student.
        score (float): Score achieved by the student (0 to 100).
        
    Returns:
        bool: True if insert was successful, False otherwise.
    """
    cleaned_name = name.strip()
    if not cleaned_name:
        raise ValueError("Student name cannot be empty.")

    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Can execute AddStudent stored procedure or parameterized INSERT
            sql_query = "INSERT INTO dbo.Students (Name, Score) VALUES (?, ?);"
            cursor.execute(sql_query, (cleaned_name, float(score)))
            return True
    finally:
        connection.close()
