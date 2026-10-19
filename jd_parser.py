import re


def clean_text(text):
    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_requirements(job_description):

    text = clean_text(job_description)

    requirements = {
        "skills": [],
        "responsibilities": [],
        "education": []
    }

    # --------------------------------
    # Skills
    # --------------------------------

    skill_keywords = [
        "python",
        "java",
        "c++",
        "javascript",
        "sql",
        "machine learning",
        "deep learning",
        "generative ai",
        "genai",
        "nlp",
        "natural language processing",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "pandas",
        "numpy",
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes",
        "fastapi",
        "flask",
        "django",
        "git"
    ]

    for skill in skill_keywords:

        if skill in text:
            requirements["skills"].append(skill)

    # --------------------------------
    # Responsibilities
    # --------------------------------

    responsibility_phrases = [
        "develop machine learning models",
        "build machine learning models",
        "train machine learning models",
        "machine learning models",

        "data processing pipelines",
        "data preprocessing",
        "data processing",

        "model training",
        "model evaluation",
        "model development",

        "api development",
        "api integration",

        "cloud deployment",
        "model deployment",
        "deploy machine learning systems",
        "deployment of ml systems",

        "ai applications",
        "machine learning applications",

        "anomaly detection",
        "intelligent recommendations",

        "analyze data",
        "data analysis",

        "develop",
        "build",
        "design",
        "implement",
        "train",
        "evaluate",
        "deploy",
        "analyze",
        "preprocess",
        "optimize",
        "integrate"
    ]

    for phrase in responsibility_phrases:

        if phrase in text:
            requirements["responsibilities"].append(
                phrase
            )

    # --------------------------------
    # Education
    # --------------------------------

    education_keywords = [
        "bachelor",
        "b.tech",
        "btech",
        "b.e",
        "b.e.",
        "bachelor's",
        "bachelor’s",
        "computer science",
        "artificial intelligence",
        "data science",
        "related field",
        "degree",
        "master",
        "m.tech",
        "mtech"
    ]

    for keyword in education_keywords:

        if keyword in text:
            requirements["education"].append(
                keyword
            )

    return requirements