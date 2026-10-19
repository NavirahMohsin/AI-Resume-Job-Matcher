import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


SECTION_PROFILES = {
    "summary": """
    Professional summary, profile, objective, career objective,
    introduction, overview of the candidate.
    """,

    "experience": """
    Work experience, professional experience, employment history,
    internships, jobs, responsibilities, company roles and
    professional positions.
    """,

    "projects": """
    Projects, personal projects, academic projects, project work,
    applications developed, systems built, research projects.
    """,

    "skills": """
    Technical skills, programming languages, frameworks, libraries,
    databases, cloud platforms, tools, technologies and technical
    competencies.
    """,

    "education": """
    Education, academic background, degree, university, college,
    school and academic qualifications.
    """,

    "certifications": """
    Certifications, professional certificates, completed courses,
    credentials and training programs.
    """,

    "achievements": """
    Achievements, awards, honors, competitions, hackathons,
    accomplishments and recognitions.
    """
}


KNOWN_HEADINGS = {
    "summary": [
        "summary",
        "profile",
        "professional summary",
        "career objective",
        "objective",
        "about me"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "work history",
        "employment history",
        "internship",
        "internships",
        "internship experience"
    ],

    "projects": [
        "projects",
        "project",
        "personal projects",
        "academic projects",
        "selected projects",
        "key projects",
        "project experience"
    ],

    "skills": [
        "skills",
        "technical skills",
        "technical expertise",
        "core skills",
        "key skills",
        "technologies",
        "tech stack",
        "tools and technologies"
    ],

    "education": [
        "education",
        "educational background",
        "academic background",
        "academic qualifications",
        "educational qualifications",
        "qualifications"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "courses",
        "training"
    ],

    "achievements": [
        "achievements",
        "awards",
        "honors",
        "accomplishments"
    ]
}


def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_line(line):
    line = line.strip()
    line = re.sub(r"\s+", " ", line)

    return line


def normalize_heading(line):

    line = line.lower().strip()

    line = line.replace("&", "and")

    line = re.sub(r"[^a-z0-9\s]", " ", line)

    line = re.sub(r"\s+", " ", line)

    return line.strip()


def detect_known_heading(line):

    normalized_line = normalize_heading(line)

    if not normalized_line:
        return None

    for section, headings in KNOWN_HEADINGS.items():

        for heading in headings:

            if normalized_line == normalize_heading(heading):
                return section

    return None


def is_content_pattern(line):
    """
    Detect lines that are clearly content rather than headings.
    """

    # Category-style skill lines:
    #
    # Programming: Python, Java, C
    # AI/ML: Machine Learning, Generative AI
    # Tools: Git, Linux, Excel

    if ":" in line:
        return True

    # Contact information
    if "@" in line:
        return True

    # Phone numbers
    if re.search(r"\+?\d[\d\s().-]{7,}", line):
        return True

    # URLs / social links
    lower_line = line.lower()

    if "http://" in lower_line or "https://" in lower_line:
        return True

    if "linkedin" in lower_line or "github" in lower_line:
        return True

    # Date ranges
    if re.search(
        r"\b(19|20)\d{2}\b.*\b(19|20)\d{2}\b",
        line
    ):
        return True

    # Academic indicators
    academic_terms = [
        "cgpa",
        "gpa",
        "university",
        "college",
        "institute",
        "b.tech",
        "btech",
        "bsc",
        "b.sc",
        "m.tech",
        "mtech",
        "degree",
        "bachelor",
        "master"
    ]

    if any(term in lower_line for term in academic_terms):
        return True

    return False


def is_heading_candidate(line):

    line = clean_line(line)

    if not line:
        return False

    # Never semantically classify obvious content
    if is_content_pattern(line):
        return False

    words = line.split()

    # Section headings are generally short
    if len(words) > 6:
        return False

    # Full sentences are not headings
    if line.endswith("."):
        return False

    return True


def classify_heading(line):

    section_names = list(SECTION_PROFILES.keys())

    heading_embedding = model.encode(
        [line],
        normalize_embeddings=True
    )

    profile_embeddings = model.encode(
        [
            SECTION_PROFILES[section]
            for section in section_names
        ],
        normalize_embeddings=True
    )

    similarities = cosine_similarity(
        heading_embedding,
        profile_embeddings
    )[0]

    best_index = similarities.argmax()

    best_section = section_names[best_index]

    confidence = float(similarities[best_index])

    return best_section, confidence


def parse_resume(text):

    text = clean_text(text)

    lines = text.split("\n")

    sections = {}

    current_section = "unknown"

    sections[current_section] = []

    for line in lines:

        line = clean_line(line)

        if not line:
            continue

        # ---------------------------------------
        # 1. Explicit heading
        # ---------------------------------------

        known_section = detect_known_heading(line)

        if known_section:

            current_section = known_section

            if current_section not in sections:
                sections[current_section] = []

            continue

        # ---------------------------------------
        # 2. Semantic fallback
        # ---------------------------------------

        if is_heading_candidate(line):

            section, confidence = classify_heading(line)

            # Only accept strong semantic predictions
            if confidence >= 0.60:

                current_section = section

                if current_section not in sections:
                    sections[current_section] = []

                continue

        # ---------------------------------------
        # 3. Normal content
        # ---------------------------------------

        sections[current_section].append(line)

    # Convert lists into strings
    for section in sections:

        sections[section] = "\n".join(
            sections[section]
        ).strip()

    return sections