import sqlite3

DATABASE = "skilltrack.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()


    # -----------------------------
    # STUDENT INFORMATION
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skills TEXT,
            projects TEXT,
            target_job TEXT,
            experience TEXT,
            roadmap TEXT,
            resume_completed INTEGER DEFAULT 0,
            interview_completed INTEGER DEFAULT 0
        )
    """)


    # -----------------------------
    # LEARNING PROGRESS
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            skill_name TEXT,
            status TEXT,
            FOREIGN KEY (student_id)
            REFERENCES students(id)
        )
    """)


    # -----------------------------
    # CHECK OLD DATABASE COLUMNS
    # -----------------------------

    cursor.execute("PRAGMA table_info(students)")

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]


    # Add roadmap if missing

    if "roadmap" not in columns:

        cursor.execute(
            "ALTER TABLE students ADD COLUMN roadmap TEXT"
        )


    # Add resume_completed if missing

    if "resume_completed" not in columns:

        cursor.execute(
            "ALTER TABLE students ADD COLUMN resume_completed INTEGER DEFAULT 0"
        )


    # Add interview_completed if missing

    if "interview_completed" not in columns:

        cursor.execute(
            "ALTER TABLE students ADD COLUMN interview_completed INTEGER DEFAULT 0"
        )


    connection.commit()

    connection.close()


if __name__ == "__main__":

    create_tables()

    print("Database updated successfully!")