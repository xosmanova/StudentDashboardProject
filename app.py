"""
app.py
Presentation / UI layer for the Student Performance Dashboard using Streamlit.
Connects through the business logic layer (services.py) and database layer (database.py).
Adheres strictly to Clean Code principles and MVC/Layered architecture.
"""

import pandas as pd
import streamlit as st

import config
import database
import services


def render_header() -> None:
    """Renders the dashboard page header and branding."""
    st.title(f"{config.APP_ICON} {config.APP_TITLE}")
    st.caption(f"{config.APP_SUBTITLE} | {database.get_active_database_mode()}")
    st.divider()


def render_statistics_section(students: list[dict]) -> None:
    """
    Renders high-level KPI metric cards for students.
    Displays: Total Students, Average Score, Highest Score, Lowest Score.
    """
    stats = services.calculate_statistics(students)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Students",
            value=stats["total_students"],
            help="Ümumi qeydiyyatdan keçmiş tələbələrin sayı",
        )
    with col2:
        st.metric(
            label="Average Score",
            value=f"{stats['average_score']:.1f}",
            help="Tələbələrin orta bal göstəricisi",
        )
    with col3:
        st.metric(
            label="Highest Score",
            value=f"{int(stats['highest_score']) if stats['highest_score'].is_integer() else stats['highest_score']}",
            help="Maksimum toplanmış bal",
        )
    with col4:
        st.metric(
            label="Lowest Score",
            value=f"{int(stats['lowest_score']) if stats['lowest_score'].is_integer() else stats['lowest_score']}",
            help="Minimum toplanmış bal",
        )

    st.write("")  # Vertical spacing


def render_add_student_form() -> None:
    """
    Renders form controls to collect and add a new student record to UniversityDB.
    Validates input using the business logic service before database insertion.
    """
    st.subheader("➕ Add New Student")

    with st.form("add_student_form", clear_on_submit=True):
        student_name = st.text_input(
            label="Student Name",
            placeholder="Məsələn: Ali Mammadov",
        )

        student_score = st.number_input(
            label="Score",
            min_value=float(config.MIN_VALID_SCORE),
            max_value=float(config.MAX_VALID_SCORE),
            value=75.0,
            step=1.0,
            help="0 ilə 100 arasında bal daxil edin",
        )

        submit_button = st.form_submit_button(
            label="Add Student",
            use_container_width=True,
            type="primary",
        )

        if submit_button:
            is_valid, error_message = services.validate_student_input(
                student_name, student_score
            )
            if not is_valid:
                st.error(f"Xəta: {error_message}")
            else:
                try:
                    database.add_student(name=student_name, score=student_score)
                    predicted_grade = services.calculate_grade(student_score)
                    st.success(
                        f"✅ Tələbə '{student_name.strip()}' uğurla əlavə edildi! "
                        f"(Score: {student_score}, Grade: {predicted_grade})"
                    )
                    st.rerun()
                except Exception as exc:
                    st.error(f"Verilənlər bazası xətası: {exc}")


def render_student_table_and_search(students: list[dict]) -> None:
    """
    Renders search input and student directory table with Name, Score, and Grade.
    """
    st.subheader("📋 Student Directory")

    search_query = st.text_input(
        label="Search Student",
        placeholder="Tələbə adına görə axtarış edin...",
    )

    # Filter logic: Use stored procedure search if search query provided
    if search_query.strip():
        filtered_raw = database.get_student(search_query)
        display_students = services.enrich_students_with_grade(filtered_raw)
        st.info(f"'{search_query}' üçün tapılan nəticələr: {len(display_students)}")
    else:
        display_students = services.enrich_students_with_grade(students)

    if not display_students:
        st.warning("Göstərmək üçün heç bir tələbə qeydi tapılmadı.")
        return

    # Convert to DataFrame for clean presentation
    display_df = pd.DataFrame(display_students)[["Name", "Score", "Grade"]]

    # Format Score cleanly if whole number
    display_df["Score"] = display_df["Score"].apply(
        lambda x: int(x) if isinstance(x, (int, float)) and x.is_integer() else x
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Name": st.column_config.TextColumn("Name", width="medium"),
            "Score": st.column_config.NumberColumn("Score", width="small"),
            "Grade": st.column_config.TextColumn("Grade", width="small"),
        },
    )


def render_performance_chart(students: list[dict]) -> None:
    """Renders a visual bar chart of students and their scores."""
    if not students:
        return

    st.subheader("📊 Performance Visualization")
    chart_df = pd.DataFrame(students)[["Name", "Score"]].sort_values(
        by="Score", ascending=False
    )
    st.bar_chart(data=chart_df.set_index("Name"), color="#1E88E5")


def render_architecture_info() -> None:
    """Collapsible expander documenting Clean Code and 3-tier architecture."""
    with st.expander("ℹ️ Layihə Memarlığı & Clean Code İzahı"):
        st.markdown(
            """
            **Mərhələli Memarlıq (Layered Architecture):**
            - **SQL Server (`UniversityDB`):** Cədvəllər və `GetStudentResult` Stored Procedure.
            - **Database Layer (`database.py`):** `create_connection()`, `add_student()`, `get_students()`, `get_student()`.
            - **Business Logic Layer (`services.py`):** `calculate_grade()`, `calculate_statistics()`, input validation.
            - **Presentation Layer (`app.py`):** Streamlit interfeysi (`st.metric`, `st.dataframe`, `st.text_input`).
            
            **Clean Code Prinsipləri:**
            - **Meaningful Names:** Məqsədyönlü, aydın dəyişən və funksiya adları.
            - **Single Responsibility (SRP):** Hər modul və funksiya yalnız bir məsuliyyət daşıyır.
            - **DRY & KISS:** Kod təkrarı yoxdur, sadə və effektiv həllər.
            - **No Magic Numbers:** Bütün hədd qiymətləri `config.py` daxilində sabitlər kimi təyin olunub.
            """
        )


def main() -> None:
    """Main application entry point."""
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=config.APP_ICON,
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    render_header()

    # Fetch data safely from Database layer
    try:
        raw_students = database.get_students()
    except Exception as exc:
        st.error(
            f"⚠️ SQL Server ilə əlaqə qurularkən xəta baş verdi: {exc}\n\n"
            f"Zəhmət olmasa SQL Server xidmətinin ('SQLEXPRESS') işlək olduğundan "
            f"və 'UniversityDB' bazasının yaradıldığından əmin olun."
        )
        return

    # 1. Statistics Cards Section
    render_statistics_section(raw_students)

    st.divider()

    # 2. Main Content: Left Column (Add Student) | Right Column (Directory Table)
    left_col, right_col = st.columns([1, 2], gap="large")

    with left_col:
        render_add_student_form()

    with right_col:
        render_student_table_and_search(raw_students)

    st.divider()

    # 3. Analytics Chart
    render_performance_chart(raw_students)

    # 4. Architecture Info
    render_architecture_info()


if __name__ == "__main__":
    main()
