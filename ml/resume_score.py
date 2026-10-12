def calculate_resume_score(text, skills):
    score = 0
    feedback = []

    text_lower = text.lower()

    # 1. Skills — 30 points
    if len(skills) >= 8:
        score += 30
    elif len(skills) >= 5:
        score += 20
    elif len(skills) >= 3:
        score += 10
    else:
        feedback.append("Add more technical skills.")

    # 2. Education — 15 points
    if any(word in text_lower for word in [
        "education",
        "bachelor",
        "degree",
        "b.tech",
        "b.e",
        "engineering"
    ]):
        score += 15
    else:
        feedback.append("Add a clear Education section.")

    # 3. Projects — 20 points
    if any(word in text_lower for word in [
        "project",
        "projects"
    ]):
        score += 20
    else:
        feedback.append("Add projects to your resume.")

    # 4. Experience — 15 points
    if any(word in text_lower for word in [
        "experience",
        "internship",
        "intern"
    ]):
        score += 15
    else:
        feedback.append("Add internship or experience details.")

    # 5. Certifications — 10 points
    if any(word in text_lower for word in [
        "certification",
        "certifications",
        "certificate"
    ]):
        score += 10
    else:
        feedback.append("Add relevant certifications if available.")

    # 6. Contact information — 10 points
    if "@" in text_lower:
        score += 5

    if any(word in text_lower for word in [
        "linkedin",
        "github"
    ]):
        score += 5
    else:
        feedback.append("Add GitHub or LinkedIn profile.")

    return {
        "score": score,
        "feedback": feedback
    }


if __name__ == "__main__":

    sample_text = """
    Education
    Bachelor of Engineering in Computer Science

    Projects
    AI Career Intelligence

    Internship
    Software Development Intern

    Certifications
    Python Certification

    GitHub
    LinkedIn
    """

    sample_skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "JavaScript",
        "Git"
    ]

    result = calculate_resume_score(
        sample_text,
        sample_skills
    )

    print("Resume Score")
    print("============")

    print("Score:", result["score"], "/ 100")

    print("\nFeedback:")

    for item in result["feedback"]:
        print("-", item)