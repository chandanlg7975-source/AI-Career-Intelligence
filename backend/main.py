from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os

from ml.resume_parser import extract_text_from_pdf
from ml.skill_extractor import extract_skills
from ml.job_recommender import recommend_jobs
from ml.skill_gap import analyze_skill_gap
from ml.learning_recommender import recommend_resources
from ml.resume_score import calculate_resume_score
from ml.rag_search import search_knowledge
from ml.mock_interview import (
    get_interview_questions,
    evaluate_answer
)

from web_search import search_web


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Career Intelligence API",
    description="AI-powered career intelligence backend",
    version="1.0"
)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Career Intelligence is working!"
    }


# ============================================================
# RESUME ANALYZER
# ============================================================

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):

        return {
            "error": "Please upload a PDF resume."
        }

    file_path = f"uploaded_{file.filename}"

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    text = extract_text_from_pdf(
        file_path
    )

    skills = extract_skills(
        text
    )

    job_recommendations = recommend_jobs(
        skills
    )

    if job_recommendations:

        best_job = job_recommendations[0]

        best_job_name = best_job["job"]

    else:

        best_job_name = "AI Engineer"

    skill_gap_job = best_job_name

    if best_job_name == "ML Engineer":

        skill_gap_job = "Machine Learning Engineer"

    skill_gap = analyze_skill_gap(
        skills,
        skill_gap_job
    )

    skill_gap["job"] = best_job_name

    learning_resources = recommend_resources(
        skill_gap["missing_skills"]
    )

    resume_score = calculate_resume_score(
        text,
        skills
    )

    try:

        os.remove(file_path)

    except OSError:

        pass

    return {

        "filename": file.filename,

        "resume_text": text,

        "skills": skills,

        "job_recommendations":
            job_recommendations,

        "skill_gap":
            skill_gap,

        "learning_resources":
            learning_resources,

        "resume_score":
            resume_score
    }


# ============================================================
# JOB QUERY DETECTION
# ============================================================

def is_job_query(question):

    question_lower = question.lower()

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

    return any(
        keyword in question_lower
        for keyword in job_keywords
    )


# ============================================================
# FORMAT WEB JOB RESULTS
# ============================================================

def format_web_job_results(
    results,
    question
):

    if not results:

        return (
            "## 🔎 Web Job Search\n\n"
            f"I couldn't find current web results "
            f"for **{question}**.\n\n"
            "Try a more specific search such as:\n"
            "- AI Engineer jobs in India\n"
            "- Machine Learning Engineer jobs for freshers\n"
            "- Python Developer jobs in Bangalore\n"
            "- Data Scientist jobs in India"
        )

    response = [

        "## 🌐 Current Web Job Opportunities",

        f"### 🔎 Search: {question}",

        "",

        f"Found **{len(results)} web results**.",

        ""
    ]

    for index, result in enumerate(
        results,
        start=1
    ):

        title = result.get(
            "title",
            "Job Opportunity"
        )

        url = result.get(
            "url",
            ""
        )

        content = result.get(
            "content",
            result.get(
                "snippet",
                ""
            )
        )

        if len(content) > 350:

            content = (
                content[:350]
                + "..."
            )

        response.append(
            f"### {index}. 💼 {title}"
        )

        if content:

            response.append(
                content
            )

        if url:

            response.append(
                f"🔗 **[View Job / Open Web Page]"
                f"({url})**"
            )

        response.append("")

    response.append(
        "---\n"
        "💡 **Tip:** Always open the original "
        "listing to verify eligibility, location, "
        "experience, salary and application details."
    )

    return "\n".join(
        response
    )


# ============================================================
# DIRECT WEB SEARCH ENDPOINT
# ============================================================

@app.get("/web-search")
def web_search_endpoint(
    query: str
):

    if not query.strip():

        return {

            "query": query,

            "results": [],

            "answer":
                "Please enter a job search query."
        }

    try:

        results = search_web(
            query,
            max_results=8
        )

        normalized_results = []

        for result in results:

            title = result.get(
                "title",
                "Job Opportunity"
            )

            url = result.get(
                "url",
                ""
            )

            snippet = result.get(
                "snippet",
                result.get(
                    "content",
                    ""
                )
            )

            normalized_results.append({

                "title": title,

                "url": url,

                "snippet": snippet
            })

        return {

            "query": query,

            "results": normalized_results,

            "answer": format_web_job_results(
                results,
                query
            )
        }

    except Exception as error:

        return {

            "query": query,

            "results": [],

            "answer":
                "Web search failed.",

            "error": str(error)
        }


# ============================================================
# CAREER ASSISTANT
# ============================================================

@app.get("/career-assistant")
def career_assistant(
    question: str
):

    if not question.strip():

        return {

            "answer":
                "Please enter a career question."
        }

    # --------------------------------------------------------
    # CURRENT JOB SEARCH
    # --------------------------------------------------------

    if is_job_query(question):

        try:

            web_results = search_web(
                question,
                max_results=8
            )

            answer = format_web_job_results(
                web_results,
                question
            )

            return {

                "question":
                    question,

                "type":
                    "web_job_search",

                "answer":
                    answer,

                "results":
                    web_results
            }

        except Exception as error:

            return {

                "question":
                    question,

                "type":
                    "web_job_search",

                "answer":
                    "Web search failed.",

                "results": [],

                "error":
                    str(error)
            }

    # --------------------------------------------------------
    # NORMAL CAREER KNOWLEDGE / RAG
    # --------------------------------------------------------

    answer = search_knowledge(
        question
    )

    return {

        "question":
            question,

        "type":
            "career_knowledge",

        "answer":
            answer
    }


# ============================================================
# MOCK INTERVIEW
# ============================================================

@app.get("/mock-interview/{job_role}")
def mock_interview(
    job_role: str
):

    questions = get_interview_questions(
        job_role
    )

    return {

        "job_role":
            job_role,

        "total_questions":
            len(questions),

        "questions":
            questions
    }


# ============================================================
# EVALUATE INTERVIEW ANSWER
# ============================================================

@app.post("/evaluate-answer")
async def evaluate_interview_answer(
    answer: str = Form(...),
    question: str = Form(...)
):

    result = evaluate_answer(
        answer,
        question
    )

    return {

        "answer":
            answer,

        "question":
            question,

        "score":
            result["score"],

        "feedback":
            result["feedback"],

        "matched_keywords":
            result.get(
                "matched_keywords",
                []
            ),

        "word_count":
            result.get(
                "word_count",
                0
            )
    }