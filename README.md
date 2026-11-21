# skill-track
AI-Powered Student Career Planner – Personalized learning roadmaps based on current skills, projects &amp; target job

# 🎯 Skill-Track — AI Career Planner for Students

Skill-Track is an AI-powered career planning web application designed to help college students understand their skill gaps, create personalized learning roadmaps, prepare for interviews, and build internship-ready resumes.

## 🚀 Features

- 🤖 **AI Career Roadmap**
  - Analyzes the student's skills, projects, experience, and target job.
  - Generates a personalized career roadmap.

- 📊 **Skill Progress Tracking**
  - Track important career skills.
  - Mark skills as Not Started, In Progress, or Completed.

- 📅 **Weekly Learning Plan**
  - Generates a personalized 7-day learning plan.
  - Includes learning tasks, practice tasks, and estimated time.

- 📄 **AI Resume Builder**
  - Generates an ATS-friendly resume based on student information.
  - Supports internship-focused resume creation.

- 🎤 **AI Interview Preparation**
  - Generates technical, project-based, and HR interview questions.
  - Provides suggested answers and interview tips.

- 🎯 **Career Readiness Score**
  - Calculates a readiness score based on:
    - Skill progress
    - Projects
    - Career roadmap
    - Interview and resume preparation

- 💾 **Student Progress Database**
  - Uses SQLite to store student profiles and learning progress.

## 🛠️ Technologies Used

- **Python**
- **Flask**
- **SQLite**
- **HTML**
- **CSS**
- **JavaScript**
- **OpenAI API**
- **Git & GitHub**

## 🏗️ Project Structure

```text
Skill-Track/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── weekly_plan.html
│   ├── resume.html
│   ├── interview.html
│   └── readiness.html
│
└── skilltrack.db
```

> `skilltrack.db` is excluded from GitHub using `.gitignore`.

## ⚙️ How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Harshitha-P23/skill-track.git
```

### 2. Open the project

```bash
cd skill-track
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows:**

```powershell
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Set your OpenAI API key

In PowerShell:

```powershell
$env:OPENAI_API_KEY="YOUR_API_KEY"
```

**Never commit or share your actual API key.**

### 7. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## 🔄 How Skill-Track Works

```text
Student Profile
      ↓
AI Career Analysis
      ↓
Skill Gap Analysis
      ↓
Personalized Roadmap
      ↓
Weekly Learning Plan
      ↓
Skill Progress Tracking
      ↓
Resume + Interview Preparation
      ↓
Career Readiness Score
```

## 🎯 Target Users

Skill-Track is mainly designed for:

- College students
- Computer science students
- Students preparing for internships
- Students preparing for technical interviews
- Beginners who need a structured career roadmap

## 🌟 Future Improvements

- 🌐 Deploy the application online
- 📈 Add visual progress charts
- 🧑‍💻 Add interactive AI interview practice
- 👤 Add student profile editing
- 📥 Add downloadable resume files
- 🔐 Add user authentication
- 🎨 Add dark/light mode
- 📊 Add detailed career analytics

## 👩‍💻 Project

**Skill-Track — AI Career Planner for Students**

Built as a student software project using Python, Flask, SQLite, HTML/CSS, JavaScript, and AI.
