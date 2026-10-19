import json
import re


def load_skills():
    with open("data/skills.json", "r", encoding="utf-8") as file:
        return json.load(file)


def extract_skills(text):
    text = text.lower()

    skills_data = load_skills()

    found_skills = []

    for category, skills in skills_data.items():

        for skill in skills:

            pattern = r"\b" + re.escape(skill.lower()) + r"\b"

            if re.search(pattern, text):
                found_skills.append(skill)

    return sorted(set(found_skills))


def normalize_skills(skills):
    """
    Convert specific technologies into broader skill categories.
    """

    normalization_map = {
        "postgresql": "sql",
        "mysql": "sql",

        "pytorch": "deep learning",
        "tensorflow": "deep learning",
        "keras": "deep learning",

        "xgboost": "machine learning",
        "lightgbm": "machine learning",
        "scikit-learn": "machine learning",

        "aws lambda": "aws",
        "aws ec2": "aws",
        "aws s3": "aws",

        "fastapi": "backend",
        "django": "backend",
        "flask": "backend",

        "react": "frontend",
        "vue.js": "frontend",
        "angular": "frontend",

        "langchain": "llm",
        "rag": "llm",
        "retrieval augmented generation": "llm"
    }

    normalized = set()

    for skill in skills:

        skill_lower = skill.lower()

        normalized.add(skill_lower)

        if skill_lower in normalization_map:
            normalized.add(normalization_map[skill_lower])

    return sorted(normalized)


def compare_skills(resume_skills, job_skills):

    resume_normalized = set(
        normalize_skills(resume_skills)
    )

    job_normalized = set(
        normalize_skills(job_skills)
    )

    matching = sorted(
        resume_normalized.intersection(job_normalized)
    )

    missing = sorted(
        job_normalized - resume_normalized
    )

    return matching, missing

