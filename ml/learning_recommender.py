RESOURCES = {
    "Python": {
        "type": "Course",
        "resource": "Python for Beginners",
        "url": "https://www.python.org/about/gettingstarted/"
    },

    "Machine Learning": {
        "type": "Course",
        "resource": "Machine Learning by Google",
        "url": "https://developers.google.com/machine-learning/crash-course"
    },

    "Deep Learning": {
        "type": "Course",
        "resource": "Deep Learning Specialization",
        "url": "https://www.coursera.org/specializations/deep-learning"
    },

    "TensorFlow": {
        "type": "Documentation",
        "resource": "TensorFlow Tutorials",
        "url": "https://www.tensorflow.org/tutorials"
    },

    "NLP": {
        "type": "Course",
        "resource": "Natural Language Processing",
        "url": "https://huggingface.co/learn/nlp-course"
    },

    "SQL": {
        "type": "Course",
        "resource": "SQL Tutorial",
        "url": "https://www.w3schools.com/sql/"
    },

    "Computer Vision": {
        "type": "Course",
        "resource": "Computer Vision",
        "url": "https://opencv.org/university/"
    },

    "Pandas": {
        "type": "Documentation",
        "resource": "Pandas Getting Started",
        "url": "https://pandas.pydata.org/docs/getting_started/"
    },

    "NumPy": {
        "type": "Documentation",
        "resource": "NumPy Quickstart",
        "url": "https://numpy.org/doc/stable/user/quickstart.html"
    }
}


def recommend_resources(missing_skills):

    recommendations = []

    for skill in missing_skills:

        if skill in RESOURCES:

            recommendations.append({
                "skill": skill,
                "type": RESOURCES[skill]["type"],
                "resource": RESOURCES[skill]["resource"],
                "url": RESOURCES[skill]["url"]
            })

    return recommendations


if __name__ == "__main__":

    missing_skills = [
        "Deep Learning",
        "TensorFlow",
        "NLP"
    ]

    recommendations = recommend_resources(missing_skills)

    print("\nLearning Recommendations")
    print("========================")

    for item in recommendations:

        print("\nSkill:", item["skill"])
        print("Type:", item["type"])
        print("Resource:", item["resource"])
        print("URL:", item["url"])