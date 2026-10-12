import streamlit as st
import requests
import pandas as pd

from auth import show_auth_page, logout

from database.database import (
    create_tables,
    save_resume_analysis,
    get_resume_history,
    get_latest_resume_analysis,
    get_latest_interview_result,
    save_interview_result
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Career Intelligence",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# PROFESSIONAL UI STYLING
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

h1, h2, h3 {
    font-weight: 700;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    min-height: 42px;
}

.stMetric {
    background-color: #1f2937;
    padding: 15px;
    border-radius: 12px;
}

div[data-testid="stFileUploader"] {
    border: 1px dashed #4b5563;
    border-radius: 12px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DATABASE
# =========================================================

create_tables()

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "interview_questions" not in st.session_state:
    st.session_state["interview_questions"] = []

if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0

if "answer_evaluated" not in st.session_state:
    st.session_state["answer_evaluated"] = False

if "last_result" not in st.session_state:
    st.session_state["last_result"] = None

if "interview_scores" not in st.session_state:
    st.session_state["interview_scores"] = []

if "interview_completed" not in st.session_state:
    st.session_state["interview_completed"] = False

if "selected_role" not in st.session_state:
    st.session_state["selected_role"] = "AI Engineer"

if "interview_saved" not in st.session_state:
    st.session_state["interview_saved"] = False

# =========================================================
# LOGIN
# =========================================================

if not st.session_state["logged_in"]:
    show_auth_page()
    st.stop()

user = st.session_state["user"]

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🤖 AI Career Intelligence")

st.sidebar.write(
    f"Welcome, **{user['name']}** 👋"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "📄 Resume Analyzer",
        "💬 Career Assistant",
        "🎯 Mock Interview"
    ]
)

st.sidebar.markdown("---")

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):
    logout()
    st.rerun()

# =========================================================
# BACKEND
# =========================================================

BACKEND_URL = "http://127.0.0.1:8000"

# =========================================================
# GET REQUEST
# =========================================================

def request_get(endpoint, params=None):

    try:

        response = requests.get(
            f"{BACKEND_URL}{endpoint}",
            params=params,
            timeout=60
        )

        return response

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Backend server is not running.\n\n"
            "Please start FastAPI using:\n\n"
            "`uvicorn backend.main:app --reload`"
        )

        return None

    except Exception as error:

        st.error(
            f"❌ Connection error: {error}"
        )

        return None


# =========================================================
# POST REQUEST
# =========================================================

def request_post(endpoint, data=None, files=None):

    try:

        response = requests.post(
            f"{BACKEND_URL}{endpoint}",
            data=data,
            files=files,
            timeout=120
        )

        return response

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Backend server is not running.\n\n"
            "Please start FastAPI using:\n\n"
            "`uvicorn backend.main:app --reload`"
        )

        return None

    except Exception as error:

        st.error(
            f"❌ Connection error: {error}"
        )

        return None


# =========================================================
# SCORE HELPER
# =========================================================

def get_numeric_score(score_data):

    if score_data is None:
        return 0.0

    if isinstance(score_data, (int, float)):
        return float(score_data)

    if isinstance(score_data, dict):

        possible_keys = [
            "score",
            "resume_score",
            "interview_score",
            "average_score"
        ]

        for key in possible_keys:

            if key in score_data:

                value = score_data[key]

                if isinstance(value, (int, float)):
                    return float(value)

                try:
                    return float(value)
                except:
                    return 0.0

    try:
        return float(score_data)

    except:
        return 0.0


# =========================================================
# PERFORMANCE HELPER
# =========================================================

def get_performance_level(score):

    score = get_numeric_score(score)

    if score >= 90:
        return "Excellent 🌟"

    elif score >= 75:
        return "Very Good 👍"

    elif score >= 60:
        return "Good 🙂"

    elif score >= 40:
        return "Needs Improvement ⚡"

    else:
        return "Beginner 📚"


# =========================================================
# LIST HELPER
# =========================================================

def convert_to_list(value):

    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, str):

        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    return []


# =========================================================
# DASHBOARD
# =========================================================

if page == "📊 Dashboard":

    st.title("📊 Career Analytics")

    st.write(
        "Track your resume strength, interview performance "
        "and career progress."
    )

    st.markdown("---")

    # -----------------------------------------------------
    # LATEST RESUME
    # -----------------------------------------------------

    latest_resume = None

    try:

        latest_resume = get_latest_resume_analysis(
            user["id"]
        )

    except Exception:

        latest_resume = None

    resume_score = 0.0
    recommended_role = "Not analyzed yet"

    resume_skills = []
    resume_missing_skills = []

    if latest_resume:

        try:

            resume_score = get_numeric_score(
                latest_resume["resume_score"]
            )

        except:

            resume_score = 0.0

        try:

            recommended_role = latest_resume[
                "recommended_role"
            ]

        except:

            recommended_role = "Not analyzed yet"

        try:

            resume_skills = convert_to_list(
                latest_resume["skills"]
            )

        except:

            resume_skills = []

        try:

            resume_missing_skills = convert_to_list(
                latest_resume["missing_skills"]
            )

        except:

            resume_missing_skills = []

    # -----------------------------------------------------
    # LATEST INTERVIEW
    # -----------------------------------------------------

    latest_interview = None

    try:

        latest_interview = get_latest_interview_result(
            user["id"]
        )

    except Exception:

        latest_interview = None

    interview_score = 0.0

    if latest_interview:

        try:

            interview_score = get_numeric_score(
                latest_interview["interview_score"]
            )

        except:

            try:

                interview_score = get_numeric_score(
                    latest_interview["average_score"]
                )

            except:

                interview_score = 0.0

    # -----------------------------------------------------
    # CAREER READINESS
    # -----------------------------------------------------

    career_readiness = (
        resume_score * 0.5
        +
        interview_score * 0.5
    )

    # -----------------------------------------------------
    # MAIN METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📄 Resume Score",
            f"{resume_score:.0f}/100",
            border=True
        )

    with col2:

        st.metric(
            "🎯 Interview Score",
            f"{interview_score:.0f}/100",
            border=True
        )

    with col3:

        st.metric(
            "💼 Recommended Role",
            recommended_role,
            border=True
        )

    with col4:

        st.metric(
            "🚀 Career Readiness",
            f"{career_readiness:.0f}%",
            border=True
        )

    # -----------------------------------------------------
    # CAREER STATUS
    # -----------------------------------------------------

    st.markdown("---")

    st.subheader("🚀 Career Status")

    col1, col2 = st.columns(2)

    with col1:

        st.write("### 📄 Resume Performance")

        st.progress(
            min(
                max(
                    resume_score / 100,
                    0.0
                ),
                1.0
            )
        )

        st.write(
            get_performance_level(
                resume_score
            )
        )

    with col2:

        st.write("### 🎯 Interview Performance")

        st.progress(
            min(
                max(
                    interview_score / 100,
                    0.0
                ),
                1.0
            )
        )

        st.write(
            get_performance_level(
                interview_score
            )
        )

    # -----------------------------------------------------
    # SKILLS ANALYTICS
    # -----------------------------------------------------

    st.markdown("---")

    st.subheader(
        "🧠 Skills & Skill Gap Analytics"
    )

    skill_col1, skill_col2, skill_col3 = st.columns(3)

    with skill_col1:

        st.metric(
            "🟢 Detected Skills",
            len(resume_skills)
        )

    with skill_col2:

        st.metric(
            "🔴 Missing Skills",
            len(resume_missing_skills)
        )

    with skill_col3:

        total_skills = (
            len(resume_skills)
            +
            len(resume_missing_skills)
        )

        if total_skills > 0:

            skill_readiness = (
                len(resume_skills)
                /
                total_skills
                *
                100
            )

        else:

            skill_readiness = 0

        st.metric(
            "📈 Skill Readiness",
            f"{skill_readiness:.0f}%"
        )

    if resume_skills:

        st.write(
            "### 🟢 Current Skills"
        )

        st.write(
            ", ".join(resume_skills)
        )

    if resume_missing_skills:

        st.write(
            "### 🔴 Skills to Learn"
        )

        for skill in resume_missing_skills:

            st.write(
                f"🔴 {skill}"
            )

    # -----------------------------------------------------
    # AI CAREER ACTION PLAN
    # -----------------------------------------------------

    st.markdown("---")

    st.subheader(
        "🤖 AI Career Action Plan"
    )

    if resume_score < 60:

        st.warning(
            "📄 Your resume needs improvement."
        )

        st.write(
            "Focus on adding strong technical projects, "
            "measurable achievements and relevant AI/ML skills."
        )

    elif interview_score < 60:

        st.warning(
            "🎤 Your interview performance needs improvement."
        )

        st.write(
            "Practice technical questions, improve your "
            "explanations and complete more mock interviews."
        )

    elif career_readiness >= 80:

        st.success(
            "🌟 You are career ready!"
        )

        st.write(
            f"Your current target role is **{recommended_role}**. "
            "Continue improving your skills and start applying "
            "for internships and entry-level opportunities."
        )

    else:

        st.info(
            "📈 You are making good progress."
        )

        st.write(
            f"Keep improving your resume and interview skills "
            f"to become ready for **{recommended_role}** roles."
        )

    # -----------------------------------------------------
    # RECOMMENDED ACTIONS
    # -----------------------------------------------------

    st.markdown(
        "### 🎯 Recommended Next Actions"
    )

    action_col1, action_col2, action_col3 = st.columns(3)

    with action_col1:

        st.info(
            "📄 **Improve Resume**\n\n"
            "Add strong projects and relevant technical skills."
        )

    with action_col2:

        st.info(
            "🎤 **Practice Interviews**\n\n"
            "Complete mock interviews and improve your answers."
        )

    with action_col3:

        st.info(
            "💼 **Prepare for Jobs**\n\n"
            "Build your portfolio and start applying for internships."
        )

    # -----------------------------------------------------
    # INTERVIEW ANALYTICS
    # -----------------------------------------------------

    st.markdown("---")

    st.subheader(
        "🎯 Latest Interview Analytics"
    )

    if latest_interview:

        interview_col1, interview_col2, interview_col3 = st.columns(3)

        with interview_col1:

            st.metric(
                "Interview Score",
                f"{interview_score:.0f}/100"
            )

        with interview_col2:

            st.metric(
                "Performance",
                get_performance_level(
                    interview_score
                )
            )

        with interview_col3:

            try:

                interview_role = latest_interview[
                    "job_role"
                ]

            except:

                interview_role = "Unknown"

            st.metric(
                "Interview Role",
                interview_role
            )

        if interview_score >= 80:

            st.success(
                "🌟 Excellent interview performance!"
            )

        elif interview_score >= 60:

            st.info(
                "👍 Good performance. Keep improving "
                "your technical explanations."
            )

        else:

            st.warning(
                "📚 Continue practicing interview fundamentals."
            )

    else:

        st.info(
            "Complete a mock interview to see interview analytics."
        )

    # -----------------------------------------------------
    # RESUME HISTORY
    # -----------------------------------------------------

    st.markdown("---")

    st.subheader(
        "📚 Resume Analysis History"
    )

    try:

        history = get_resume_history(
            user["id"]
        )

        # -------------------------------------------------
        # RESUME SCORE PROGRESS
        # -------------------------------------------------

        if history:

            chart_data = []

            for item in history:

                try:

                    score = get_numeric_score(
                        item["resume_score"]
                    )

                    date = str(
                        item["analysis_date"]
                    )

                    chart_data.append(
                        {
                            "Date": date,
                            "Resume Score": score
                        }
                    )

                except Exception:

                    continue

            if chart_data:

                chart_data.reverse()

                chart_df = pd.DataFrame(
                    chart_data
                )

                st.subheader(
                    "📈 Resume Score Progress"
                )

                st.line_chart(
                    chart_df,
                    x="Date",
                    y="Resume Score"
                )

                st.caption(
                    "📊 Your resume score across previous analyses."
                )

        # -------------------------------------------------
        # HISTORY LIST
        # -------------------------------------------------

        if history:

            for item in history:

                try:

                    score = get_numeric_score(
                        item["resume_score"]
                    )

                except:

                    score = 0.0

                try:

                    role = item[
                        "recommended_role"
                    ]

                except:

                    role = "Unknown"

                try:

                    date = item[
                        "analysis_date"
                    ]

                except:

                    date = "Unknown"

                with st.container():

                    c1, c2, c3 = st.columns(3)

                    with c1:

                        st.write(
                            f"📄 **Score:** "
                            f"{score:.0f}/100"
                        )

                    with c2:

                        st.write(
                            f"💼 **Role:** {role}"
                        )

                    with c3:

                        st.write(
                            f"📅 **Date:** {date}"
                        )

                    st.divider()

        else:

            st.info(
                "No resume analysis found yet. "
                "Upload your resume in Resume Analyzer."
            )

    except Exception:

        st.info(
            "Resume history will appear after your first analysis."
        )


# =========================================================
# RESUME ANALYZER
# =========================================================

elif page == "📄 Resume Analyzer":

    st.title(
        "📄 AI Resume Analyzer"
    )

    st.write(
        "Upload your PDF resume to analyze your skills, "
        "career opportunities and missing skills."
    )

    uploaded_file = st.file_uploader(
        "Upload your PDF Resume",
        type=["pdf"]
    )

    if uploaded_file:

        if st.button(
            "🔍 Analyze Resume",
            use_container_width=True
        ):

            with st.spinner(
                "🤖 AI is analyzing your resume..."
            ):

                response = request_post(
                    "/upload-resume",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    }
                )

            if response is not None:

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "✅ Resume analysis completed!"
                    )

                    # -------------------------------------
                    # SCORE
                    # -------------------------------------

                    resume_score_data = result.get(
                        "resume_score",
                        0
                    )

                    resume_score = get_numeric_score(
                        resume_score_data
                    )

                    st.subheader(
                        "📊 Resume Score"
                    )

                    st.metric(
                        "Resume Score",
                        f"{resume_score:.0f}/100"
                    )

                    st.progress(
                        min(
                            max(
                                resume_score / 100,
                                0.0
                            ),
                            1.0
                        )
                    )

                    if isinstance(
                        resume_score_data,
                        dict
                    ):

                        feedback = resume_score_data.get(
                            "feedback"
                        )

                        if feedback:

                            st.info(
                                f"💡 {feedback}"
                            )

                    st.markdown("---")

                    # -------------------------------------
                    # SKILLS
                    # -------------------------------------

                    st.subheader(
                        "🧠 Detected Skills"
                    )

                    skills = result.get(
                        "skills",
                        []
                    )

                    if skills:

                        st.write(
                            ", ".join(skills)
                        )

                    else:

                        st.info(
                            "No skills detected."
                        )

                    # -------------------------------------
                    # JOB ROLES
                    # -------------------------------------

                    st.subheader(
                        "💼 Recommended Career Roles"
                    )

                    job_recommendations = result.get(
                        "job_recommendations",
                        []
                    )

                    if job_recommendations:

                        for index, job in enumerate(
                            job_recommendations,
                            start=1
                        ):

                            job_name = job.get(
                                "job",
                                "Unknown Role"
                            )

                            job_score = get_numeric_score(
                                job.get(
                                    "score",
                                    0
                                )
                            )

                            matched_skills = job.get(
                                "matched_skills",
                                []
                            )

                            st.write(
                                f"### {index}. {job_name}"
                            )

                            st.progress(
                                min(
                                    max(
                                        job_score / 100,
                                        0.0
                                    ),
                                    1.0
                                )
                            )

                            st.write(
                                f"Match Score: "
                                f"**{job_score:.1f}%**"
                            )

                            if matched_skills:

                                st.write(
                                    "Matched skills: "
                                    +
                                    ", ".join(
                                        matched_skills
                                    )
                                )

                    st.markdown("---")

                    # -------------------------------------
                    # MISSING SKILLS
                    # -------------------------------------

                    st.subheader(
                        "⚠️ Missing Skills"
                    )

                    skill_gap = result.get(
                        "skill_gap",
                        {}
                    )

                    missing_skills = skill_gap.get(
                        "missing_skills",
                        []
                    )

                    if missing_skills:

                        for skill in missing_skills:

                            st.write(
                                f"🔴 {skill}"
                            )

                    else:

                        st.success(
                            "🎉 No major missing skills found!"
                        )

                    st.markdown("---")

                    # -------------------------------------
                    # LEARNING RESOURCES
                    # -------------------------------------

                    st.subheader(
                        "📚 Recommended Learning Resources"
                    )

                    learning_resources = result.get(
                        "learning_resources",
                        []
                    )

                    if learning_resources:

                        for resource in learning_resources:

                            if isinstance(
                                resource,
                                dict
                            ):

                                skill = resource.get(
                                    "skill",
                                    "Skill"
                                )

                                title = resource.get(
                                    "title",
                                    "Learning Resource"
                                )

                                url = resource.get(
                                    "url",
                                    ""
                                )

                                st.write(
                                    f"### 📘 {skill}"
                                )

                                st.write(
                                    title
                                )

                                if url:

                                    st.markdown(
                                        f"[🔗 Open Learning Resource]"
                                        f"({url})"
                                    )

                            else:

                                st.write(
                                    f"📘 {resource}"
                                )

                    # -------------------------------------
                    # SAVE ANALYSIS
                    # -------------------------------------

                    try:

                        best_role = (
                            job_recommendations[0]["job"]
                            if job_recommendations
                            else "AI Engineer"
                        )

                        if best_role == "ML Engineer":

                            best_role_for_db = (
                                "Machine Learning Engineer"
                            )

                        else:

                            best_role_for_db = best_role

                        save_resume_analysis(
                            user["id"],
                            resume_score,
                            best_role_for_db,
                            ", ".join(skills),
                            ", ".join(missing_skills)
                        )

                        st.success(
                            "💾 Resume analysis saved to your career history."
                        )

                    except Exception as error:

                        st.warning(
                            f"Analysis completed, but "
                            f"history could not be saved: {error}"
                        )

                else:

                    st.error(
                        f"Backend error: "
                        f"{response.status_code}"
                    )


# =========================================================
# CAREER ASSISTANT
# =========================================================

elif page == "💬 Career Assistant":

    st.title(
        "💬 AI Career Assistant"
    )

    st.write(
        "Ask career questions, learn about AI/ML roles "
        "or search for current job opportunities."
    )

    question = st.text_area(
        "Ask your career question",
        placeholder=(
            "Example:\n"
            "What skills do I need to become an AI Engineer?\n"
            "AI Engineer jobs in India\n"
            "Machine Learning jobs for freshers"
        ),
        height=120
    )

    if st.button(
        "🤖 Ask AI",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            job_keywords = [
                "job",
                "jobs",
                "job opening",
                "job openings",
                "vacancy",
                "vacancies",
                "hiring",
                "hire",
                "career opening",
                "career openings",
                "employment",
                "apply",
                "work opportunity",
                "work opportunities",
                "position",
                "positions",
                "internship",
                "internships"
            ]

            is_job_query = any(
                keyword in question.lower()
                for keyword in job_keywords
            )

            if is_job_query:

                with st.spinner(
                    "🌐 Searching current web results..."
                ):

                    response = request_get(
                        "/web-search",
                        params={
                            "query": question
                        }
                    )

            else:

                with st.spinner(
                    "🤖 Searching career knowledge..."
                ):

                    response = request_get(
                        "/career-assistant",
                        params={
                            "question": question
                        }
                    )

            if response is not None:

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No answer available."
                    )

                    st.markdown(
                        answer
                    )

                else:

                    st.error(
                        f"Backend error: "
                        f"{response.status_code}"
                    )


# =========================================================
# MOCK INTERVIEW
# =========================================================

elif page == "🎯 Mock Interview":

    st.title(
        "🎯 AI Mock Interview"
    )

    st.write(
        "Practice realistic interview questions "
        "and receive AI-style feedback."
    )

    # =====================================================
    # INTERVIEW COMPLETED
    # =====================================================

    if st.session_state[
        "interview_completed"
    ]:

        st.success(
            "🎉 Interview completed!"
        )

        scores = st.session_state[
            "interview_scores"
        ]

        if scores:

            numeric_scores = [
                get_numeric_score(score)
                for score in scores
            ]

            average_score = (
                sum(numeric_scores)
                /
                len(numeric_scores)
            )

        else:

            numeric_scores = []

            average_score = 0.0

        # =================================================
        # FINAL REPORT
        # =================================================

        st.subheader(
            "📊 Final Interview Assessment"
        )

        st.write(
            f"**Role:** "
            f"{st.session_state['selected_role']}"
        )

        st.markdown("---")

        # =================================================
        # SCORE SUMMARY
        # =================================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🎯 Overall Score",
                f"{average_score:.1f}/100",
                border=True
            )

        with col2:

            st.metric(
                "📝 Questions",
                len(scores),
                border=True
            )

        with col3:

            st.metric(
                "📈 Performance",
                get_performance_level(
                    average_score
                ),
                border=True
            )

        with col4:

            if average_score >= 80:

                readiness = "Career Ready 🚀"

            elif average_score >= 60:

                readiness = "Almost Ready 👍"

            else:

                readiness = "Keep Practicing 📚"

            st.metric(
                "💼 Readiness",
                readiness,
                border=True
            )

        # =================================================
        # OVERALL PERFORMANCE
        # =================================================

        st.markdown("---")

        st.subheader(
            "🚀 Overall Interview Performance"
        )

        st.progress(
            min(
                max(
                    average_score / 100,
                    0.0
                ),
                1.0
            )
        )

        if average_score >= 80:

            st.success(
                "🌟 Excellent performance! "
                "Your answers show strong interview readiness."
            )

        elif average_score >= 60:

            st.info(
                "👍 Good performance! "
                "You have a solid foundation, but there is "
                "still room to improve your technical explanations."
            )

        else:

            st.warning(
                "📚 Keep practicing! "
                "Focus on fundamentals, technical concepts "
                "and explaining your answers clearly."
            )

        # =================================================
        # SCORE BREAKDOWN
        # =================================================

        st.markdown("---")

        st.subheader(
            "📈 Question-by-Question Score"
        )

        for index, score in enumerate(
            numeric_scores,
            start=1
        ):

            score = get_numeric_score(
                score
            )

            score_col1, score_col2 = st.columns(
                [4, 1]
            )

            with score_col1:

                st.write(
                    f"Question {index}"
                )

                st.progress(
                    min(
                        max(
                            score / 100,
                            0.0
                        ),
                        1.0
                    )
                )

            with score_col2:

                st.write(
                    f"**{score:.0f}/100**"
                )

        # =================================================
        # STRENGTHS
        # =================================================

        st.markdown("---")

        st.subheader(
            "💪 Your Strengths"
        )

        if average_score >= 80:

            st.success(
                "✅ Strong understanding of interview concepts."
            )

            st.success(
                "✅ Good answer quality."
            )

            st.success(
                "✅ Good technical communication."
            )

        elif average_score >= 60:

            st.success(
                "✅ You have a good basic understanding."
            )

            st.success(
                "✅ You are able to answer many technical questions."
            )

            st.success(
                "✅ Your interview foundation is developing."
            )

        else:

            st.info(
                "📚 You are building your interview foundation."
            )

            st.info(
                "💡 Continue practicing basic technical concepts."
            )

        # =================================================
        # AREAS TO IMPROVE
        # =================================================

        st.markdown("---")

        st.subheader(
            "⚠️ Areas to Improve"
        )

        if average_score < 60:

            st.warning(
                "🔴 Strengthen your technical fundamentals."
            )

            st.warning(
                "🔴 Practice explaining concepts in simple language."
            )

            st.warning(
                "🔴 Practice more mock interviews."
            )

        elif average_score < 80:

            st.warning(
                "🟡 Improve the depth of your technical answers."
            )

            st.warning(
                "🟡 Add practical examples when answering questions."
            )

            st.warning(
                "🟡 Work on confidence and communication."
            )

        else:

            st.info(
                "🟢 Keep improving advanced technical knowledge."
            )

            st.info(
                "🟢 Practice real-world interview scenarios."
            )

            st.info(
                "🟢 Continue preparing for company-specific interviews."
            )

        # =================================================
        # ACTION PLAN
        # =================================================

        st.markdown("---")

        st.subheader(
            "🎯 Recommended Action Plan"
        )

        if average_score >= 80:

            st.write(
                "🚀 **Step 1:** Start applying for internships "
                "and entry-level roles."
            )

            st.write(
                "🧠 **Step 2:** Practice advanced AI/ML "
                "interview questions."
            )

            st.write(
                "💼 **Step 3:** Prepare company-specific "
                "interview questions."
            )

        elif average_score >= 60:

            st.write(
                "📚 **Step 1:** Strengthen your core "
                "technical concepts."
            )

            st.write(
                "🎤 **Step 2:** Complete more mock interviews."
            )

            st.write(
                "💻 **Step 3:** Build practical AI/ML projects."
            )

        else:

            st.write(
                "📚 **Step 1:** Learn and revise Python, "
                "AI and ML fundamentals."
            )

            st.write(
                "🎤 **Step 2:** Practice answering basic "
                "interview questions."
            )

            st.write(
                "💻 **Step 3:** Build small projects to "
                "improve practical knowledge."
            )

        # =================================================
        # SAVE RESULT ONLY ONCE
        # =================================================

        if not st.session_state[
            "interview_saved"
        ]:

            try:

                role = st.session_state[
                    "selected_role"
                ]

                performance = get_performance_level(
                    average_score
                )

                save_interview_result(
                    user_id=user["id"],
                    job_role=role,
                    average_score=average_score,
                    total_questions=len(scores),
                    performance_level=performance,
                    interview_score=average_score
                )

                st.session_state[
                    "interview_saved"
                ] = True

            except Exception:

                pass

        # =================================================
        # START NEW INTERVIEW
        # =================================================

        st.markdown("---")

        if st.button(
            "🔄 Start New Interview",
            use_container_width=True
        ):

            st.session_state[
                "interview_questions"
            ] = []

            st.session_state[
                "current_question"
            ] = 0

            st.session_state[
                "answer_evaluated"
            ] = False

            st.session_state[
                "last_result"
            ] = None

            st.session_state[
                "interview_scores"
            ] = []

            st.session_state[
                "interview_completed"
            ] = False

            st.session_state[
                "interview_saved"
            ] = False

            st.rerun()

    # =====================================================
    # INTERVIEW NOT STARTED
    # =====================================================

    elif not st.session_state[
        "interview_questions"
    ]:

        job_role = st.selectbox(
            "Select Interview Role",
            [
                "AI Engineer",
                "Machine Learning Engineer",
                "Data Scientist",
                "Data Analyst",
                "Backend Developer",
                "GenAI Engineer"
            ]
        )

        st.session_state[
            "selected_role"
        ] = job_role

        st.markdown("---")

        st.info(
            "The interview contains 10 randomly selected "
            "questions from a larger question bank."
        )

        if st.button(
            "🎯 Generate Interview",
            use_container_width=True
        ):

            with st.spinner(
                "Preparing your interview..."
            ):

                response = request_get(
                    f"/mock-interview/{job_role}"
                )

            if response is not None:

                if response.status_code == 200:

                    data = response.json()

                    questions = data.get(
                        "questions",
                        []
                    )

                    if len(questions) == 0:

                        st.error(
                            "❌ No interview questions received "
                            "from backend."
                        )

                    else:

                        st.session_state[
                            "interview_questions"
                        ] = questions

                        st.session_state[
                            "current_question"
                        ] = 0

                        st.session_state[
                            "answer_evaluated"
                        ] = False

                        st.session_state[
                            "last_result"
                        ] = None

                        st.session_state[
                            "interview_scores"
                        ] = []

                        st.session_state[
                            "interview_completed"
                        ] = False

                        st.session_state[
                            "interview_saved"
                        ] = False

                        st.rerun()

                else:

                    st.error(
                        f"Backend error: "
                        f"{response.status_code}"
                    )

    # =====================================================
    # ACTIVE INTERVIEW
    # =====================================================

    else:

        questions = st.session_state[
            "interview_questions"
        ]

        current_index = st.session_state[
            "current_question"
        ]

        total_questions = len(
            questions
        )

        # -------------------------------------------------
        # SAFETY CHECK
        # -------------------------------------------------

        if current_index >= total_questions:

            st.session_state[
                "interview_completed"
            ] = True

            st.rerun()

        question = questions[
            current_index
        ]

        st.subheader(
            f"{st.session_state['selected_role']} "
            "Mock Interview"
        )

        st.write(
            f"### Question {current_index + 1} "
            f"of {total_questions}"
        )

        st.progress(
            (current_index + 1)
            /
            total_questions
        )

        st.markdown("---")

        st.write(
            f"## ❓ Question {current_index + 1}"
        )

        st.info(
            question
        )

        # -------------------------------------------------
        # ANSWER
        # -------------------------------------------------

        answer = st.text_area(
            "✍️ Your Answer",
            placeholder=(
                "Type your interview answer here..."
            ),
            height=180,
            key=f"answer_{current_index}"
        )

        # -------------------------------------------------
        # EVALUATE
        # -------------------------------------------------

        if not st.session_state[
            "answer_evaluated"
        ]:

            if st.button(
                "✅ Evaluate Answer",
                use_container_width=True
            ):

                if not answer.strip():

                    st.warning(
                        "Please enter your answer first."
                    )

                else:

                    with st.spinner(
                        "🤖 Evaluating your answer..."
                    ):

                        evaluate_response = request_post(
                            "/evaluate-answer",
                            data={
                                "answer": answer,
                                "question": question
                            }
                        )

                    if evaluate_response is not None:

                        if (
                            evaluate_response.status_code
                            == 200
                        ):

                            result = (
                                evaluate_response.json()
                            )

                            st.session_state[
                                "last_result"
                            ] = result

                            score = get_numeric_score(
                                result.get(
                                    "score",
                                    0
                                )
                            )

                            current_scores = (
                                st.session_state[
                                    "interview_scores"
                                ]
                            )

                            if (
                                len(current_scores)
                                <= current_index
                            ):

                                current_scores.append(
                                    score
                                )

                            else:

                                current_scores[
                                    current_index
                                ] = score

                            st.session_state[
                                "interview_scores"
                            ] = current_scores

                            st.session_state[
                                "answer_evaluated"
                            ] = True

                            st.rerun()

                        else:

                            st.error(
                                "Unable to evaluate "
                                "your answer."
                            )

        # -------------------------------------------------
        # SHOW FEEDBACK
        # -------------------------------------------------

        if st.session_state[
            "answer_evaluated"
        ]:

            result = st.session_state[
                "last_result"
            ]

            if result:

                score = get_numeric_score(
                    result.get(
                        "score",
                        0
                    )
                )

                st.markdown("---")

                st.subheader(
                    "📊 Answer Evaluation"
                )

                feedback_col1, feedback_col2 = st.columns(2)

                with feedback_col1:

                    st.metric(
                        "Score",
                        f"{score:.0f}/100"
                    )

                with feedback_col2:

                    st.metric(
                        "Word Count",
                        result.get(
                            "word_count",
                            0
                        )
                    )

                st.progress(
                    min(
                        max(
                            score / 100,
                            0.0
                        ),
                        1.0
                    )
                )

                feedback = result.get(
                    "feedback",
                    ""
                )

                if feedback:

                    st.info(
                        f"💡 {feedback}"
                    )

                matched_keywords = result.get(
                    "matched_keywords",
                    []
                )

                if matched_keywords:

                    st.write(
                        "### 🧠 Matched Keywords"
                    )

                    st.write(
                        ", ".join(
                            matched_keywords
                        )
                    )

                st.markdown("---")

                # =========================================
                # NEXT QUESTION
                # =========================================

                if current_index < total_questions - 1:

                    if st.button(
                        "➡️ Next Question",
                        use_container_width=True
                    ):

                        st.session_state[
                            "current_question"
                        ] += 1

                        st.session_state[
                            "answer_evaluated"
                        ] = False

                        st.session_state[
                            "last_result"
                        ] = None

                        st.rerun()

                # =========================================
                # FINAL REPORT
                # =========================================

                else:

                    if st.button(
                        "📊 View Final Interview Report",
                        use_container_width=True
                    ):

                        st.session_state[
                            "interview_completed"
                        ] = True

                        st.rerun()