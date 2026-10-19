from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from skills import extract_skills

model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(text1, text2):
    embedding1 = model.encode([text1])
    embedding2 = model.encode([text2])

    similarity = cosine_similarity(embedding1, embedding2)[0][0]

    return float(similarity)


def calculate_match_score(similarity):
    return round(max(0.0, min(float(similarity), 1.0)) * 100, 2)


def _to_text(value):
    if isinstance(value, list):
        return " ".join(str(item) for item in value)

    if isinstance(value, dict):
        return " ".join(str(item) for item in value.values())

    return str(value or "")


def _keyword_coverage(resume_text, target_text):
    """
    Measures how much of the target text is explicitly represented
    in the resume section.
    """
    resume_text = resume_text.lower()
    target_text = target_text.lower()

    target_words = {
        word.strip(".,:;()[]{}")
        for word in target_text.split()
        if len(word.strip(".,:;()[]{}")) > 2
    }

    if not target_words:
        return None

    matched_words = {
        word for word in target_words
        if word in resume_text
    }

    return len(matched_words) / len(target_words)


def _section_score(resume_section, target_text):
    if not resume_section or not target_text.strip():
        return None

    semantic_score = calculate_similarity(
        resume_section,
        target_text,
    )

    coverage = _keyword_coverage(
        resume_section,
        target_text,
    )

    if coverage is None:
        return calculate_match_score(semantic_score)

    # Explicit requirement coverage is weighted more heavily than
    # general semantic similarity.
    combined_score = (
        (coverage * 0.65)
        + (semantic_score * 0.35)
    )

    return round(max(0.0, min(combined_score, 1.0)) * 100, 2)


def calculate_targeted_scores(
    resume_text,
    resume_sections,
    requirements,
    job_description=None,
):
    """
    Calculate scores against relevant job-description content.

    Sections that are not present in the resume are omitted rather than
    being incorrectly represented as zero.
    """
    resume_sections = resume_sections or {}
    requirements = requirements or {}

    scores = {}

    resume_skills = extract_skills(resume_text)
    job_skills = requirements.get("skills", [])

    # Skills are measured using explicit skill coverage rather than
    # comparing the entire resume against the entire job description.
    if resume_skills and job_skills:
        resume_skill_set = {
            skill.lower() for skill in resume_skills
        }
        job_skill_set = {
            skill.lower() for skill in job_skills
        }

        coverage = len(
            resume_skill_set.intersection(job_skill_set)
        ) / len(job_skill_set)

        scores["skills"] = round(coverage * 100, 2)

    # Experience should be compared with responsibilities and
    # role expectations, not with education or the full JD.
    experience_target = _to_text(
        requirements.get("responsibilities", [])
    )

    if not experience_target and job_description:
        experience_target = job_description

    experience_section = _to_text(
        resume_sections.get("experience", "")
    )

    experience_score = _section_score(
        experience_section,
        experience_target,
    )

    if experience_score is not None:
        scores["experience"] = experience_score

    # Projects are compared with responsibilities/objectives. This is
    # useful for students, but it is not treated as professional experience.
    projects_section = _to_text(
        resume_sections.get("projects", "")
    )

    projects_target = _to_text(
        requirements.get("responsibilities", [])
    )

    projects_score = _section_score(
        projects_section,
        projects_target,
    )

    if projects_score is not None:
        scores["projects"] = projects_score

    education_section = _to_text(
        resume_sections.get("education", "")
    )

    education_target = _to_text(
        requirements.get("education", [])
    )

    education_score = _section_score(
        education_section,
        education_target,
    )

    if education_score is not None:
        scores["education"] = education_score

    return scores