JOB_SKILLS = {

    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Computer Vision",
        "NLP",
        "TensorFlow"
    ],

    "ML Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Pandas",
        "NumPy",
        "TensorFlow",
        "SQL",
        "Scikit-learn"
    ],

    "Data Scientist": [
        "Python",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "SQL",
        "Statistics",
        "Data Science"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Excel",
        "Statistics",
        "Data Analysis"
    ],

    "Backend Developer": [
        "Python",
        "SQL",
        "APIs",
        "FastAPI",
        "Django",
        "Database"
    ],

    "GenAI Engineer": [
        "Python",
        "Machine Learning",
        "Artificial Intelligence",
        "NLP",
        "Deep Learning",
        "LLM",
        "RAG"
    ]
}


def analyze_skill_gap(user_skills, job):

    required_skills = JOB_SKILLS.get(job, [])

    user_skills_lower = [
        skill.lower()
        for skill in user_skills
    ]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill.lower() in user_skills_lower:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    if len(required_skills) > 0:

        score = (
            len(matched_skills)
            / len(required_skills)
        ) * 100

    else:

        score = 0

    return {
        "job": job,
        "score": round(score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }


if __name__ == "__main__":

    sample_skills = [
        "Python",
        "Machine Learning",
        "Pandas",
        "NumPy"
    ]

    result = analyze_skill_gap(
        sample_skills,
        "ML Engineer"
    )

    print("Skill Gap Analysis")
    print("===================")

    print("Job:", result["job"])

    print("Score:", result["score"])

    print("Matched Skills:")
    print(result["matched_skills"])

    print("Missing Skills:")
    print(result["missing_skills"])