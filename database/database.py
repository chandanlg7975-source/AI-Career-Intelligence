import sqlite3
import bcrypt


DATABASE_NAME = "career_intelligence.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


# ============================================================
# CREATE TABLES + SAFE DATABASE MIGRATION
# ============================================================

def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------------------------
    # USERS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # --------------------------------------------------------
    # RESUME ANALYSIS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resume_score REAL DEFAULT 0,
            recommended_role TEXT,
            skills TEXT,
            missing_skills TEXT,
            analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # --------------------------------------------------------
    # INTERVIEW RESULTS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_role TEXT,
            interview_score REAL,
            total_questions INTEGER,
            interview_date TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.commit()

    # ========================================================
    # SAFE MIGRATION FOR OLD DATABASE
    # ========================================================

    # Get existing interview_results columns
    cursor.execute("PRAGMA table_info(interview_results)")
    columns = cursor.fetchall()

    existing_columns = [
        column["name"]
        for column in columns
    ]

    # Add missing columns WITHOUT DEFAULT values
    # because SQLite does not allow CURRENT_TIMESTAMP
    # as an ALTER TABLE default.

    if "job_role" not in existing_columns:

        cursor.execute("""
            ALTER TABLE interview_results
            ADD COLUMN job_role TEXT
        """)

    if "interview_score" not in existing_columns:

        cursor.execute("""
            ALTER TABLE interview_results
            ADD COLUMN interview_score REAL
        """)

    if "total_questions" not in existing_columns:

        cursor.execute("""
            ALTER TABLE interview_results
            ADD COLUMN total_questions INTEGER
        """)

    if "interview_date" not in existing_columns:

        cursor.execute("""
            ALTER TABLE interview_results
            ADD COLUMN interview_date TIMESTAMP
        """)

    connection.commit()
    connection.close()


# ============================================================
# REGISTER USER
# ============================================================

def register_user(name, email, password):

    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                hashed_password
            )
        )

        connection.commit()

        return True, "Registration successful!"

    except sqlite3.IntegrityError:

        return False, "Email already registered."

    finally:

        connection.close()


# ============================================================
# LOGIN USER
# ============================================================

def login_user(email, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    stored_password = user["password"]

    if bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password.encode("utf-8")
    ):

        return {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }

    return None


# ============================================================
# SAVE RESUME ANALYSIS
# ============================================================

def save_resume_analysis(
    user_id,
    resume_score,
    recommended_role,
    skills,
    missing_skills
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO resume_analysis
        (
            user_id,
            resume_score,
            recommended_role,
            skills,
            missing_skills
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            resume_score,
            recommended_role,
            skills,
            missing_skills
        )
    )

    connection.commit()
    connection.close()


# ============================================================
# GET RESUME HISTORY
# ============================================================

def get_resume_history(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM resume_analysis
        WHERE user_id = ?
        ORDER BY analysis_date DESC
        """,
        (user_id,)
    )

    results = cursor.fetchall()

    connection.close()

    return results


# ============================================================
# GET LATEST RESUME ANALYSIS
# ============================================================

def get_latest_resume_analysis(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM resume_analysis
        WHERE user_id = ?
        ORDER BY analysis_date DESC, id DESC
        LIMIT 1
        """,
        (user_id,)
    )

    result = cursor.fetchone()

    connection.close()

    return result


# ============================================================
# SAVE INTERVIEW RESULT
# ============================================================

def save_interview_result(
    user_id,
    job_role,
    interview_score,
    total_questions
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO interview_results
        (
            user_id,
            job_role,
            interview_score,
            total_questions,
            interview_date
        )
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
        (
            user_id,
            job_role,
            interview_score,
            total_questions
        )
    )

    connection.commit()
    connection.close()


# ============================================================
# GET LATEST INTERVIEW RESULT
# ============================================================

def get_latest_interview_result(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            user_id,
            job_role,
            interview_score,
            total_questions,
            interview_date
        FROM interview_results
        WHERE user_id = ?
        ORDER BY
            CASE
                WHEN interview_date IS NULL THEN 1
                ELSE 0
            END,
            interview_date DESC,
            id DESC
        LIMIT 1
        """,
        (user_id,)
    )

    result = cursor.fetchone()

    connection.close()

    return result


# ============================================================
# DATABASE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DATABASE TEST")
    print("=" * 60)

    create_tables()

    print("✅ Database tables are ready!")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        PRAGMA table_info(interview_results)
    """)

    columns = cursor.fetchall()

    print("\nInterview Results Columns:")

    for column in columns:
        print(
            f"✅ {column['name']} "
            f"({column['type']})"
        )

    connection.close()

    print("\n" + "=" * 60)
    print("DATABASE TEST COMPLETED")
    print("=" * 60)