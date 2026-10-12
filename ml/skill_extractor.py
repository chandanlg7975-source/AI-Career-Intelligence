import re


SKILLS = [
    "Python",
    "Java",
    "C++",
    "C#",
    "C",
    "JavaScript",
    "TypeScript",
    "SQL",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "FastAPI",
    "Django",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "NLP",
    "Natural Language Processing",
    "Computer Vision",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Streamlit",
    "SQLite",
    "MySQL",
    "MongoDB",
    "Git",
    "GitHub",
    "Docker",
    "Generative AI",
    "RAG",
    "Large Language Models"
]


def extract_skills(text):
    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill == "C":
            pattern = r"\bc\b"
        else:
            pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills


if __name__ == "__main__":

    sample_text = """
    I am a Computer Science student.
    I know Python, Java, C++, JavaScript, SQL,
    Machine Learning, React, Git and Docker.
    """

    skills = extract_skills(sample_text)

    print("Detected Skills")
    print("===============")

    for skill in skills:
        print("-", skill)