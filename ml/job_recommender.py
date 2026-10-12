from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


JOB_ROLES = {
    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "NLP",
        "Computer Vision",
        "TensorFlow",
        "PyTorch"
    ],

    "ML Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Pandas",
        "NumPy"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "Statistics",
        "Data Visualization"
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
        "FastAPI",
        "Django",
        "SQL",
        "MySQL",
        "MongoDB",
        "REST API",
        "Docker",
        "Git"
    ],

    "GenAI Engineer": [
        "Python",
        "Generative AI",
        "LLM",
        "RAG",
        "NLP",
        "Machine Learning",
        "Deep Learning",
        "Embeddings",
        "Vector Database"
    ]
}


def recommend_jobs(user_skills):

    # Convert user skills into one text document
    user_text = " ".join(user_skills)

    # Create text for every job role
    job_names = list(JOB_ROLES.keys())

    job_texts = [
        " ".join(JOB_ROLES[job])
        for job in job_names
    ]

    # Combine user skills + job descriptions
    all_texts = [user_text] + job_texts

    # TF-IDF converts words into numerical vectors
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(all_texts)

    # Compare user skills with every job role
    similarities = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )[0]

    recommendations = []

    for i, job in enumerate(job_names):

        matched_skills = []

        for skill in JOB_ROLES[job]:

            if skill.lower() in [
                s.lower() for s in user_skills
            ]:
                matched_skills.append(skill)

        score = similarities[i] * 100

        recommendations.append({
            "job": job,
            "score": round(score, 2),
            "matched_skills": matched_skills
        })

    # Highest similarity first
    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations


if __name__ == "__main__":

    sample_skills = [
        "Python",
        "Machine Learning",
        "Computer Vision",
        "SQL"
    ]

    results = recommend_jobs(sample_skills)

    print("\nTF-IDF Career Recommendations")
    print("============================")

    for result in results:

        print(
            f"\n{result['job']} "
            f"→ {result['score']}%"
        )

        print(
            "Matched skills:",
            result["matched_skills"]
        )