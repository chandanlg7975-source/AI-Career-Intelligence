import random


# ============================================================
# INTERVIEW QUESTION BANK
# ============================================================

INTERVIEW_QUESTIONS = {

    "AI Engineer": [

        "What is Artificial Intelligence and how is it different from Machine Learning?",

        "What is supervised learning? Give an example.",

        "What is the difference between Machine Learning and Deep Learning?",

        "Explain overfitting and how you can prevent it.",

        "What is the difference between classification and regression?",

        "What is a confusion matrix?",

        "Explain precision, recall and F1-score.",

        "What is feature engineering and why is it important?",

        "How would you build an AI model for detecting driver drowsiness?",

        "What is the difference between TensorFlow and PyTorch?",

        "What is Natural Language Processing?",

        "What is Computer Vision?",

        "What is a neural network?",

        "Explain the concept of training and testing data.",

        "What is cross-validation?",

        "What is gradient descent?",

        "What is an activation function?",

        "What is the purpose of a loss function?",

        "How would you handle missing data in a dataset?",

        "How would you improve a machine learning model with low accuracy?",

        "What is model deployment?",

        "How can FastAPI be used in an AI project?",

        "What is the difference between AI, ML and Deep Learning?",

        "Explain the complete lifecycle of a machine learning project.",

        "How would you explain an AI project to a non-technical person?",

        "What are the ethical challenges of Artificial Intelligence?",

        "What is Generative AI?",

        "What are Large Language Models?",

        "What is RAG and why is it useful?",

        "Describe one AI project you have built."
    ],


    "ML Engineer": [

        "What is Machine Learning?",

        "What are the main types of Machine Learning?",

        "What is supervised learning?",

        "What is unsupervised learning?",

        "What is reinforcement learning?",

        "What is overfitting?",

        "What is underfitting?",

        "How do you prevent overfitting?",

        "What is cross-validation?",

        "What is feature engineering?",

        "What is feature scaling?",

        "What is normalization?",

        "What is standardization?",

        "What is a confusion matrix?",

        "Explain precision, recall and F1-score.",

        "What is ROC-AUC?",

        "What is gradient descent?",

        "What is hyperparameter tuning?",

        "What is model deployment?",

        "How do you monitor a machine learning model?",

        "What is MLOps?",

        "How would you handle an imbalanced dataset?",

        "How would you improve a model with low accuracy?",

        "What is data leakage?",

        "What is ensemble learning?",

        "Explain Random Forest.",

        "Explain the difference between bagging and boosting.",

        "What is XGBoost?",

        "Describe a machine learning project you have built.",

        "How would you deploy an ML model using FastAPI?"
    ],


    "Data Scientist": [

        "What is Data Science?",

        "What is the difference between Data Science and Machine Learning?",

        "What is exploratory data analysis?",

        "Why is data cleaning important?",

        "How do you handle missing values?",

        "How do you detect outliers?",

        "What is correlation?",

        "What is the difference between correlation and causation?",

        "What is hypothesis testing?",

        "What is a p-value?",

        "What is a confidence interval?",

        "What is regression?",

        "What is classification?",

        "What is clustering?",

        "Explain precision, recall and F1-score.",

        "What is feature engineering?",

        "What is feature selection?",

        "What is overfitting?",

        "What is cross-validation?",

        "What is SQL and why is it important for Data Scientists?",

        "What is the difference between SQL JOIN types?",

        "How do you visualize data?",

        "What is the purpose of Pandas?",

        "What is NumPy?",

        "How do you communicate insights from data?",

        "How would you handle a very large dataset?",

        "How would you build a predictive model?",

        "How do you evaluate a regression model?",

        "How do you evaluate a classification model?",

        "Describe a Data Science project you have worked on."
    ],


    "Data Analyst": [

        "What does a Data Analyst do?",

        "What is data cleaning?",

        "What is exploratory data analysis?",

        "What is SQL?",

        "What is a primary key?",

        "What is a foreign key?",

        "What is an SQL JOIN?",

        "What is the difference between WHERE and HAVING?",

        "What is GROUP BY in SQL?",

        "What is a subquery?",

        "What is Excel used for in data analysis?",

        "What is a pivot table?",

        "What is data visualization?",

        "What is a dashboard?",

        "What is the difference between mean, median and mode?",

        "What is standard deviation?",

        "What is correlation?",

        "How do you handle missing data?",

        "How do you identify outliers?",

        "What is KPI?",

        "How would you explain a data insight to a manager?",

        "How do you validate your analysis?",

        "How do you work with large datasets?",

        "What is Power BI?",

        "What is Tableau?",

        "How do you choose the right chart for data?",

        "How would you analyze sales data?",

        "How would you find trends in a dataset?",

        "What challenges have you faced while analyzing data?",

        "Describe a data analysis project you have completed."
    ],


    "Backend Developer": [

        "What is backend development?",

        "What is an API?",

        "What is REST API?",

        "What is HTTP?",

        "What is the difference between GET and POST?",

        "What are HTTP status codes?",

        "What is JSON?",

        "What is a database?",

        "What is SQL?",

        "What is the difference between SQL and NoSQL?",

        "What is a primary key?",

        "What is a foreign key?",

        "What is database normalization?",

        "What is authentication?",

        "What is authorization?",

        "What is JWT?",

        "What is hashing?",

        "Why should passwords be hashed?",

        "What is FastAPI?",

        "What is middleware?",

        "What is exception handling?",

        "How do you secure an API?",

        "What is API rate limiting?",

        "What is caching?",

        "What is Docker?",

        "What is Git?",

        "How do you debug a backend application?",

        "How would you design a login system?",

        "How would you handle thousands of API requests?",

        "Describe a backend project you have built."
    ],


    "GenAI Engineer": [

        "What is Generative AI?",

        "What is a Large Language Model?",

        "How do Large Language Models work?",

        "What is a prompt?",

        "What is prompt engineering?",

        "What is a token?",

        "What is an embedding?",

        "What is a vector database?",

        "What is RAG?",

        "Why is RAG useful?",

        "What is hallucination in Generative AI?",

        "How can hallucinations be reduced?",

        "What is fine-tuning?",

        "What is the difference between fine-tuning and RAG?",

        "What is semantic search?",

        "What is cosine similarity?",

        "What is LangChain?",

        "What is an AI agent?",

        "What is the difference between an AI agent and a chatbot?",

        "How would you build a document question-answering system?",

        "How would you build a career assistant using RAG?",

        "How would you evaluate an LLM application?",

        "What are the challenges of deploying LLM applications?",

        "How can you reduce LLM API costs?",

        "What is context window?",

        "What is temperature in LLMs?",

        "What is hallucination?",

        "What is multimodal AI?",

        "Describe a Generative AI project you have built.",

        "How would you build a production-ready GenAI application?"
    ]
}


# ============================================================
# GET INTERVIEW QUESTIONS
# ============================================================

def get_interview_questions(job_role):

    questions = INTERVIEW_QUESTIONS.get(
        job_role,
        INTERVIEW_QUESTIONS["AI Engineer"]
    )

    # Randomly select ONLY 10 questions
    number_of_questions = min(
        10,
        len(questions)
    )

    selected_questions = random.sample(
        questions,
        number_of_questions
    )

    return selected_questions


# ============================================================
# EVALUATE INTERVIEW ANSWER
# ============================================================

def evaluate_answer(answer, question):

    answer = answer.strip()

    if not answer:

        return {
            "score": 0,
            "feedback": "Please provide an answer.",
            "matched_keywords": [],
            "word_count": 0
        }

    # --------------------------------------------------------
    # Convert text into words
    # --------------------------------------------------------

    answer_words = set(
        answer.lower().replace(
            ",",
            " "
        ).replace(
            ".",
            " "
        ).split()
    )

    question_words = set(
        question.lower().replace(
            "?",
            " "
        ).replace(
            ",",
            " "
        ).split()
    )

    # --------------------------------------------------------
    # Find common technical keywords
    # --------------------------------------------------------

    technical_keywords = [
        "ai",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "python",
        "model",
        "data",
        "training",
        "testing",
        "algorithm",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "classification",
        "regression",
        "neural network",
        "tensorflow",
        "pytorch",
        "sql",
        "api",
        "fastapi",
        "database",
        "authentication",
        "authorization",
        "generative ai",
        "llm",
        "language model",
        "embedding",
        "vector database",
        "rag",
        "prompt",
        "fine tuning",
        "semantic search",
        "computer vision",
        "nlp",
        "feature",
        "overfitting",
        "cross validation",
        "deployment"
    ]

    matched_keywords = []

    answer_lower = answer.lower()

    for keyword in technical_keywords:

        if keyword in answer_lower:

            matched_keywords.append(
                keyword
            )

    # --------------------------------------------------------
    # Word count
    # --------------------------------------------------------

    word_count = len(
        answer.split()
    )

    # --------------------------------------------------------
    # Score calculation
    # --------------------------------------------------------

    score = 0

    # Answer length
    if word_count >= 100:

        score += 35

    elif word_count >= 70:

        score += 30

    elif word_count >= 40:

        score += 25

    elif word_count >= 20:

        score += 15

    else:

        score += 5

    # Technical keywords
    keyword_score = min(
        len(matched_keywords) * 7,
        35
    )

    score += keyword_score

    # Question relevance
    common_words = answer_words.intersection(
        question_words
    )

    relevance_score = min(
        len(common_words) * 3,
        20
    )

    score += relevance_score

    score = min(
        score,
        100
    )

    # --------------------------------------------------------
    # Feedback
    # --------------------------------------------------------

    if score >= 85:

        feedback = (
            "Excellent answer! You demonstrated strong "
            "technical understanding and good explanation."
        )

    elif score >= 70:

        feedback = (
            "Good answer. Your understanding is clear, "
            "but you can improve it by adding a practical "
            "example or explaining the concept in more detail."
        )

    elif score >= 55:

        feedback = (
            "Decent answer, but it needs more technical "
            "detail. Try explaining the concept step by step "
            "and include an example."
        )

    elif score >= 40:

        feedback = (
            "Your answer shows some understanding, but "
            "you need to strengthen the fundamentals and "
            "provide more relevant technical details."
        )

    else:

        feedback = (
            "Your answer needs improvement. Study the "
            "fundamental concept and try to explain it "
            "using a simple example."
        )

    return {
        "score": score,
        "feedback": feedback,
        "matched_keywords": matched_keywords,
        "word_count": word_count
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    questions = get_interview_questions(
        "AI Engineer"
    )

    print(
        f"Generated {len(questions)} questions:"
    )

    for index, question in enumerate(
        questions,
        start=1
    ):

        print(
            f"{index}. {question}"
        )