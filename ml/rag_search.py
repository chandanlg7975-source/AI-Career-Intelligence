import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ml.knowledge_loader import load_knowledge


# ============================================================
# CAREER ROLES
# ============================================================

CAREER_ROLES = [
    "AI Engineer",
    "Machine Learning Engineer",
    "Data Scientist",
    "Data Analyst",
    "GenAI Engineer",
    "Backend Developer"
]


# ============================================================
# EXTRACT CAREER SECTIONS
# ============================================================

def get_sections():

    knowledge = load_knowledge()

    if not knowledge:
        return []

    sections = []

    # Find each career-role heading and everything until
    # the next career-role heading.
    pattern = "|".join(
        re.escape(role)
        for role in CAREER_ROLES
    )

    matches = list(
        re.finditer(
            rf"(?im)^\s*({pattern})\s*$",
            knowledge
        )
    )

    if matches:

        for index, match in enumerate(matches):

            start = match.start()

            if index + 1 < len(matches):

                end = matches[index + 1].start()

            else:

                end = len(knowledge)

            section = knowledge[start:end].strip()

            if section:

                sections.append(section)

    # Fallback if headings could not be detected
    if not sections:

        sections = [
            block.strip()
            for block in knowledge.split("\n\n")
            if block.strip()
        ]

    return sections


# ============================================================
# DETECT CAREER ROLE
# ============================================================

def detect_role(question):

    question_lower = question.lower()

    # Check longer names first
    roles_sorted = sorted(
        CAREER_ROLES,
        key=len,
        reverse=True
    )

    for role in roles_sorted:

        if role.lower() in question_lower:

            return role

    # Helpful aliases
    if "machine learning" in question_lower:
        return "Machine Learning Engineer"

    if "gen ai" in question_lower:
        return "GenAI Engineer"

    if "generative ai" in question_lower:
        return "GenAI Engineer"

    return None


# ============================================================
# CLEAN / FORMAT SECTION
# ============================================================

def format_section(section, role=None):

    lines = section.splitlines()

    output = []

    first_heading_added = False

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Main career heading
        if (
            role
            and line.lower() == role.lower()
            and not first_heading_added
        ):

            output.append(
                f"## 🎯 {role}"
            )

            first_heading_added = True

            continue

        # Markdown headings
        if line.startswith("#"):

            heading = line.lstrip("#").strip()

            output.append(
                f"### 📌 {heading}"
            )

            continue

        # Lines ending with colon
        if line.endswith(":"):

            output.append(
                f"### 📌 {line[:-1]}"
            )

            continue

        # Existing bullet
        if line.startswith(("-", "*", "•")):

            output.append(
                f"- {line.lstrip('-*• ').strip()}"
            )

            continue

        # Normal content
        output.append(
            f"- {line}"
        )

    return "\n".join(output)


# ============================================================
# SEARCH KNOWLEDGE
# ============================================================

def search_knowledge(question):

    question = question.strip()

    if not question:

        return "Please enter a career question."


    sections = get_sections()

    if not sections:

        return (
            "The career knowledge base is currently empty."
        )


    # --------------------------------------------------------
    # Detect role
    # --------------------------------------------------------

    detected_role = detect_role(question)


    # --------------------------------------------------------
    # If user asks about a specific role,
    # find that complete section.
    # --------------------------------------------------------

    if detected_role:

        role_sections = []

        for section in sections:

            if detected_role.lower() in section.lower():

                role_sections.append(section)


        if role_sections:

            best_section = role_sections[0]

            formatted = format_section(
                best_section,
                detected_role
            )

            return (
                formatted
                + "\n\n"
                + "💡 **Tip:** Build 2–3 practical "
                "projects using these skills to strengthen "
                "your portfolio."
            )


    # --------------------------------------------------------
    # TF-IDF retrieval for general questions
    # --------------------------------------------------------

    documents = [
        question
    ] + sections


    try:

        vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english"
        )

        tfidf_matrix = vectorizer.fit_transform(
            documents
        )

        similarities = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:]
        )[0]

    except ValueError:

        return (
            "I could not process that question. "
            "Please try another career question."
        )


    ranked_results = sorted(
        zip(similarities, sections),
        key=lambda item: item[0],
        reverse=True
    )


    # --------------------------------------------------------
    # No useful match
    # --------------------------------------------------------

    if not ranked_results:

        return (
            "I could not find relevant information "
            "in the career knowledge base."
        )


    if ranked_results[0][0] <= 0:

        return (
            "I could not find relevant information "
            "in the career knowledge base. "
            "Try asking about AI Engineer, "
            "Machine Learning, Data Science, "
            "GenAI, or Backend Development."
        )


    # --------------------------------------------------------
    # Return best results
    # --------------------------------------------------------

    response_parts = []

    response_parts.append(
        "## 🤖 Career Assistant"
    )

    response_parts.append(
        "Here is the most relevant career guidance:"
    )


    for score, section in ranked_results[:2]:

        response_parts.append(
            format_section(section)
        )


    response_parts.append(
        "💡 **Tip:** Focus on practical projects "
        "and demonstrate your skills through GitHub."
    )


    return "\n\n".join(
        response_parts
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    question = input(
        "Ask a career question: "
    )

    answer = search_knowledge(
        question
    )

    print()
    print(
        "Career Assistant Response"
    )
    print(
        "========================="
    )
    print(answer)