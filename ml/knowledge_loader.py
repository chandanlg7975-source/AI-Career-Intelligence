from pathlib import Path


def load_knowledge():

    file_path = Path("knowledge_base/career_knowledge.txt")

    if not file_path.exists():
        return ""

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text


if __name__ == "__main__":

    knowledge = load_knowledge()

    print("Knowledge base loaded successfully!")
    print()
    print(knowledge[:500])