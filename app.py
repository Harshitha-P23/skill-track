from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import sqlite3
import os

app = Flask(__name__)

DATABASE = "skilltrack.db"

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


# -----------------------------
# DATABASE CONNECTION
# -----------------------------

def get_connection():
    return sqlite3.connect(DATABASE)


# -----------------------------
# SAVE STUDENT
# -----------------------------

def save_student(skills, projects, target_job, experience, roadmap):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (skills, projects, target_job, experience, roadmap)
        VALUES (?, ?, ?, ?, ?)
    """, (
        skills,
        projects,
        target_job,
        experience,
        roadmap
    ))

    student_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return student_id


# -----------------------------
# GET LATEST STUDENT
# -----------------------------

def get_latest_student():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, skills, projects, target_job, experience,
               roadmap, resume_completed, interview_completed
        FROM students
        ORDER BY id DESC
        LIMIT 1
    """)

    student = cursor.fetchone()

    connection.close()

    return student


# -----------------------------
# GET PROGRESS
# -----------------------------

def get_progress(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT skill_name, status
        FROM progress
        WHERE student_id = ?
    """, (student_id,))

    rows = cursor.fetchall()

    connection.close()

    progress = {}

    for skill, status in rows:
        progress[skill] = status

    return progress


# -----------------------------
# SAVE PROGRESS
# -----------------------------

def save_progress(student_id, skill_name, status):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM progress
        WHERE student_id = ?
        AND skill_name = ?
    """, (student_id, skill_name))

    existing = cursor.fetchone()

    if existing:

        cursor.execute("""
            UPDATE progress
            SET status = ?
            WHERE student_id = ?
            AND skill_name = ?
        """, (
            status,
            student_id,
            skill_name
        ))

    else:

        cursor.execute("""
            INSERT INTO progress
            (student_id, skill_name, status)
            VALUES (?, ?, ?)
        """, (
            student_id,
            skill_name,
            status
        ))

    connection.commit()
    connection.close()


# -----------------------------
# MARK RESUME COMPLETED
# -----------------------------

def mark_resume_completed(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET resume_completed = 1
        WHERE id = ?
    """, (student_id,))

    connection.commit()
    connection.close()


# -----------------------------
# MARK INTERVIEW COMPLETED
# -----------------------------

def mark_interview_completed(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET interview_completed = 1
        WHERE id = ?
    """, (student_id,))

    connection.commit()
    connection.close()


# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    roadmap = None
    error = None

    if request.method == "POST":

        skills = request.form.get("skills", "")
        projects = request.form.get("projects", "")
        target_job = request.form.get("target_job", "")
        level = request.form.get("level", "")

        prompt = f"""
You are an expert AI career advisor for college students.

Analyze this student's profile:

Skills: {skills}
Projects: {projects}
Target Job: {target_job}
Experience: {level}

Create these seven sections:

1. SKILL GAP ANALYSIS
2. PRIORITY SKILLS
3. TECHNOLOGIES TO LEARN
4. RECOMMENDED PROJECTS
5. STEP-BY-STEP LEARNING ROADMAP
6. INTERVIEW PREPARATION
7. FINAL CAREER ADVICE

Use simple language and practical recommendations.
Suitable for a college student.

Separate each section using exactly:
---
"""

        try:

            if client is None:
                raise Exception(
                    "OPENAI_API_KEY is not set."
                )

            response = client.responses.create(
                model="gpt-6-luna",
                input=prompt
            )

            roadmap = response.output_text

            student_id = save_student(
                skills,
                projects,
                target_job,
                level,
                roadmap
            )

            default_skills = [
                "Programming Fundamentals",
                "Data Structures & Algorithms",
                "Object-Oriented Programming",
                "Database / SQL",
                "Git & GitHub",
                "Problem Solving",
                "Communication & Interview Skills"
            ]

            for skill in default_skills:

                save_progress(
                    student_id,
                    skill,
                    "Not Started"
                )

        except Exception as e:

            print("ERROR:", e)

            error = f"AI Error: {str(e)}"

    return render_template(
        "index.html",
        roadmap=roadmap,
        error=error
    )


# -----------------------------
# DASHBOARD
# -----------------------------

@app.route("/dashboard")
def dashboard():

    student = get_latest_student()

    progress = {}

    if student:
        progress = get_progress(student[0])

    return render_template(
        "dashboard.html",
        student=student,
        progress=progress
    )


# -----------------------------
# UPDATE PROGRESS
# -----------------------------

@app.route("/update-progress", methods=["POST"])
def update_progress():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No data received"
        })

    student = get_latest_student()

    if not student:

        return jsonify({
            "success": False,
            "message": "No student profile found"
        })

    student_id = student[0]

    skill_name = data.get("skill_name")
    status = data.get("status")

    if not skill_name or not status:

        return jsonify({
            "success": False,
            "message": "Skill name or status missing"
        })

    save_progress(
        student_id,
        skill_name,
        status
    )

    return jsonify({
        "success": True,
        "message": "Progress updated successfully"
    })


# -----------------------------
# WEEKLY PLAN
# -----------------------------

@app.route("/weekly-plan")
def weekly_plan():

    student = get_latest_student()

    if not student:

        return render_template(
            "weekly_plan.html",
            student=None,
            plan=None,
            error="Please generate your career roadmap first."
        )

    skills = student[1]
    projects = student[2]
    target_job = student[3]
    experience = student[4]

    prompt = f"""
You are an AI learning planner for a college computer science student.

Create a practical 7-day learning plan based on:

Current Skills:
{skills}

Projects:
{projects}

Target Job:
{target_job}

Experience Level:
{experience}

Create a plan for Monday to Sunday.

For every day include:

1. Topic
2. Learning task
3. Practice task
4. Approximate time required

Keep tasks realistic for a college student.

At the end include:

WEEKLY GOAL
and
EXPECTED OUTCOME

Use simple language.
Separate each day using:
---
"""

    try:

        if client is None:
            raise Exception(
                "OPENAI_API_KEY is not set."
            )

        response = client.responses.create(
            model="gpt-6-luna",
            input=prompt
        )

        plan = response.output_text

        return render_template(
            "weekly_plan.html",
            student=student,
            plan=plan,
            error=None
        )

    except Exception as e:

        print("ERROR:", e)

        return render_template(
            "weekly_plan.html",
            student=student,
            plan=None,
            error=f"AI Error: {str(e)}"
        )


# -----------------------------
# RESUME BUILDER
# -----------------------------

@app.route("/resume", methods=["GET", "POST"])
def resume():

    resume = None
    error = None

    if request.method == "POST":

        name = request.form.get("name", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        education = request.form.get("education", "")
        skills = request.form.get("skills", "")
        projects = request.form.get("projects", "")
        target_job = request.form.get("target_job", "")
        experience = request.form.get("experience", "")
        achievements = request.form.get("achievements", "")

        prompt = f"""
You are an expert resume writer for college students.

Create a professional, ATS-friendly resume using the information below.

Name:
{name}

Email:
{email}

Phone:
{phone}

Education:
{education}

Skills:
{skills}

Projects:
{projects}

Target Job:
{target_job}

Experience:
{experience}

Achievements:
{achievements}

Create these sections:

PROFESSIONAL SUMMARY
EDUCATION
TECHNICAL SKILLS
PROJECTS
EXPERIENCE
ACHIEVEMENTS

Rules:

- Keep the language professional and simple.
- Do not invent information.
- Use strong action-oriented wording where possible.
- Make it suitable for internship applications.
- Keep the resume concise.
- Do not include unnecessary personal information.
"""

        try:

            if client is None:
                raise Exception(
                    "OPENAI_API_KEY is not set."
                )

            response = client.responses.create(
                model="gpt-6-luna",
                input=prompt
            )

            resume = response.output_text

            # Mark resume as completed
            student = get_latest_student()

            if student:
                mark_resume_completed(student[0])

        except Exception as e:

            print("ERROR:", e)

            error = f"AI Error: {str(e)}"

    return render_template(
        "resume.html",
        resume=resume,
        error=error
    )


# -----------------------------
# AI INTERVIEW PREPARATION
# -----------------------------

@app.route("/interview", methods=["GET", "POST"])
def interview():

    student = get_latest_student()

    questions = None
    error = None

    if not student:

        return render_template(
            "interview.html",
            student=None,
            questions=None,
            error="Please generate your career roadmap first."
        )

    if request.method == "POST":

        skills = student[1]
        projects = student[2]
        target_job = student[3]
        experience = student[4]

        prompt = f"""
You are an expert technical and HR interviewer
helping a college computer science student prepare
for an internship interview.

Student profile:

Skills:
{skills}

Projects:
{projects}

Target Job:
{target_job}

Experience:
{experience}

Create a personalized interview preparation set.

Include:

SECTION 1: TECHNICAL QUESTIONS

Create 5 technical questions related to the student's
skills and target job.

For every question provide:

Question:
Suggested Answer:
Interview Tip:

---

SECTION 2: PROJECT QUESTIONS

Create 3 questions that an interviewer could ask
about the student's projects.

For every question provide:

Question:
Suggested Answer:
Interview Tip:

---

SECTION 3: HR QUESTIONS

Create 5 common HR questions.

For every question provide:

Question:
Suggested Answer:
Interview Tip:

---

SECTION 4: QUICK REVISION

Give 5 important topics the student should revise
before the interview.

Use simple language suitable for a college student.

Do not invent projects, skills, achievements,
or experience that the student has not provided.
"""

        try:

            if client is None:
                raise Exception(
                    "OPENAI_API_KEY is not set."
                )

            response = client.responses.create(
                model="gpt-6-luna",
                input=prompt
            )

            questions = response.output_text

            # Mark interview preparation as completed
            student = get_latest_student()

            if student:
                mark_interview_completed(student[0])

        except Exception as e:

            print("ERROR:", e)

            error = f"AI Error: {str(e)}"

    return render_template(
        "interview.html",
        student=student,
        questions=questions,
        error=error
    )


# -----------------------------
# CAREER READINESS
# -----------------------------

@app.route("/readiness")
def readiness():

    student = get_latest_student()

    if not student:

        return render_template(
            "readiness.html",
            student=None,
            readiness_score=0,
            readiness_level="No Profile Yet",
            skill_score=0,
            project_score=0,
            roadmap_score=0,
            preparation_score=0
        )

    student_id = student[0]

    progress = get_progress(student_id)

    total_skills = 7

    completed_skills = 0

    for status in progress.values():

        if status == "Completed":
            completed_skills += 1

    skill_percentage = int(
        (completed_skills / total_skills) * 100
    )

    skill_score = int(
        (completed_skills / total_skills) * 40
    )


    # -----------------------------
    # PROJECT SCORE
    # -----------------------------

    if student[2] and student[2].strip():

        project_score = 20

    else:

        project_score = 0


    # -----------------------------
    # ROADMAP SCORE
    # -----------------------------

    if student[5] and student[5].strip():

        roadmap_score = 20

    else:

        roadmap_score = 0


    # -----------------------------
    # CAREER PREPARATION SCORE
    # -----------------------------

    preparation_score = 0

    if student[6] == 1:

        preparation_score += 10

    if student[7] == 1:

        preparation_score += 10


    # -----------------------------
    # FINAL SCORE
    # -----------------------------

    readiness_score = (
        skill_score
        + project_score
        + roadmap_score
        + preparation_score
    )


    # -----------------------------
    # READINESS LEVEL
    # -----------------------------

    if readiness_score < 40:

        readiness_level = "Beginner 🚀"

    elif readiness_score < 70:

        readiness_level = "Making Good Progress 👍"

    else:

        readiness_level = "Career Ready 🎉"


    return render_template(
        "readiness.html",
        student=student,
        readiness_score=readiness_score,
        readiness_level=readiness_level,
        skill_score=skill_percentage,
        project_score=project_score,
        roadmap_score=roadmap_score,
        preparation_score=preparation_score
    )


# -----------------------------
# RUN APPLICATION
# -----------------------------

if __name__ == "__main__":

    app.run(debug=True)