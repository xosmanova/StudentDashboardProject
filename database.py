"""
database.py
Database access layer for the Student Performance Dashboard.
Supports dual-mode operations:
  1. Primary: Microsoft SQL Server (UniversityDB via pyodbc and Stored Procedures).
  2. Cloud Fallback: Embedded UniversityDB (SQLite) for zero-configuration cloud deployment
     (e.g., Streamlit Community Cloud where local SQLEXPRESS is unreachable).

Follows Clean Code principles: Single Responsibility, DRY, and secure parameterized queries.
"""

import logging
import os
import sqlite3
from typing import Any, Optional

try:
    import pyodbc
    HAS_PYODBC = True
except ImportError:
    HAS_PYODBC = False

from config import (
    DEFAULT_DB_NAME,
    DEFAULT_DB_SERVER,
    DEFAULT_ODBC_DRIVER,
    PREFERRED_DRIVERS,
)

logger = logging.getLogger(__name__)

SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "university_cloud.db")


# ==============================================================================
# SQL Server Helper Functions
# ==============================================================================

def _detect_installed_driver() -> str:
    """Detects the best available SQL Server ODBC driver on the host system."""
    if not HAS_PYODBC:
        return DEFAULT_ODBC_DRIVER

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
    """Constructs a secure ODBC connection string using Windows Trusted Authentication."""
    selected_driver = driver or _detect_installed_driver()
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


def _try_sql_server_connection() -> Optional[Any]:
    """Attempts to connect to MSSQL Server. Returns connection object or None."""
    if not HAS_PYODBC:
        return None

    try:
        conn_str = build_connection_string()
        conn = pyodbc.connect(conn_str, timeout=2, autocommit=True)
        return conn
    except Exception as exc:
        logger.debug("SQL Server unreachable, using cloud fallback: %s", exc)
        return None


# ==============================================================================
# Cloud SQLite Fallback Database Setup (Emulating UniversityDB)
# ==============================================================================

def _init_cloud_sqlite_db() -> None:
    """Initializes SQLite database with UniversityDB schema and sample data if needed."""
    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Students (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Score REAL NOT NULL,
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        # Check if table is empty, insert required sample data
        cursor.execute("SELECT COUNT(*) FROM Students;")
        count = cursor.fetchone()[0]
        if count == 0:
            sample_students = [
                ("Ali", 85.0),
                ("Leyla", 72.0),
                ("Murad", 48.0),
                ("Aysel", 91.0),
                ("Kamran", 63.0),
            ]
            cursor.executemany(
                "INSERT INTO Students (Name, Score) VALUES (?, ?);",
                sample_students,
            )
        conn.commit()


def get_active_database_mode() -> str:
    """Returns human-readable active database engine mode."""
    mssql_conn = _try_sql_server_connection()
    if mssql_conn:
        try:
            mssql_conn.close()
        except Exception:
            pass
        return "Microsoft SQL Server (UniversityDB)"
    return "Cloud Mode (UniversityDB)"


# ==============================================================================
# Public Database Operations (Clean Code API)
# ==============================================================================

def create_connection():
    """
    Establishes and returns an active database connection.
    Prioritizes SQL Server; falls back to SQLite for cloud deployment.
    """
    mssql_conn = _try_sql_server_connection()
    if mssql_conn is not None:
        return mssql_conn

    # Fallback to SQLite (Cloud deployment mode)
    _init_cloud_sqlite_db()
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _row_to_dict(cursor: Any, row: Any) -> dict[str, Any]:
    """Helper function to map a row to a dictionary."""
    if hasattr(row, "keys"):
        return dict(row)
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))


def get_students() -> list[dict[str, Any]]:
    """
    Retrieves all students.
    Uses MSSQL GetStudentResult stored procedure if available, otherwise executes equivalent SQL.
    """
    students: list[dict[str, Any]] = []
    conn = create_connection()
    is_sqlite = isinstance(conn, sqlite3.Connection)

    try:
        cursor = conn.cursor()
        if is_sqlite:
            cursor.execute("SELECT Id, Name, Score, CreatedAt FROM Students ORDER BY Score DESC;")
        else:
            cursor.execute("EXEC dbo.GetStudentResult;")

        rows = cursor.fetchall()
        for row in rows:
            students.append(_row_to_dict(cursor, row))
    finally:
        conn.close()

    return students


def get_student(name: str) -> list[dict[str, Any]]:
    """
    Searches students matching query string.
    Uses MSSQL GetStudentResult stored procedure or SQLite parameterized LIKE query.
    """
    students: list[dict[str, Any]] = []
    cleaned_name = name.strip() if name else ""

    conn = create_connection()
    is_sqlite = isinstance(conn, sqlite3.Connection)

    try:
        cursor = conn.cursor()
        if is_sqlite:
            if not cleaned_name:
                cursor.execute("SELECT Id, Name, Score, CreatedAt FROM Students ORDER BY Score DESC;")
            else:
                cursor.execute(
                    "SELECT Id, Name, Score, CreatedAt FROM Students WHERE Name LIKE ? ORDER BY Score DESC;",
                    (f"%{cleaned_name}%",),
                )
        else:
            cursor.execute("EXEC dbo.GetStudentResult @StudentName = ?", (cleaned_name,))

        rows = cursor.fetchall()
        for row in rows:
            students.append(_row_to_dict(cursor, row))
    finally:
        conn.close()

    return students


def add_student(name: str, score: float) -> bool:
    """
    Inserts a new student record into UniversityDB.
    Uses parameterized queries to prevent SQL Injection.
    """
    cleaned_name = name.strip()
    if not cleaned_name:
        raise ValueError("Student name cannot be empty.")

    conn = create_connection()
    is_sqlite = isinstance(conn, sqlite3.Connection)

    try:
        cursor = conn.cursor()
        sql_query = "INSERT INTO Students (Name, Score) VALUES (?, ?);"
        if not is_sqlite:
            sql_query = "INSERT INTO dbo.Students (Name, Score) VALUES (?, ?);"

        cursor.execute(sql_query, (cleaned_name, float(score)))
        if is_sqlite:
            conn.commit()
        return True
    finally:
        conn.close()
