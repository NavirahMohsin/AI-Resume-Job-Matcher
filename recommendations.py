import json
import os
import re

import streamlit as st
from groq import Groq


DEFAULT_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b",
)


def _get_groq_api_key():
    try:
        return st.secrets.get("GROQ_API_KEY")
    except Exception:
        return os.getenv("GROQ_API_KEY")


def _extract_json(content):
    content = (content or "").strip()

    # Remove Markdown fences if the model returns them.
    content = re.sub(r"^```(?:json)?\s*", "", content, flags=re.IGNORECASE)
    content = re.sub(r"\s*```$", "", content).strip()

    # Extract the JSON object if explanatory text surrounds it.
    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("Groq returned no JSON object.")

    return json.loads(content[start:end + 1])


def generate_recommendations(missing_skills, job_description):
    missing_skills = sorted(
        {
            str(skill).strip()
            for skill in (missing_skills or [])
            if str(skill).strip()
        }
    )

    if not missing_skills:
        return {"items": [], "error": None}

    api_key = _get_groq_api_key()

    if not api_key:
        return {
            "items": [],
            "error": "GROQ_API_KEY is not configured in Streamlit Secrets.",
        }

    client = Groq(api_key=api_key)

    prompt = f"""
Analyze this job description and provide practical recommendations for the
missing requirements.

Missing requirements:
{json.dumps(missing_skills)}

Job description:
{job_description[:12000]}

Return valid JSON only:
{{
  "recommendations": [
    {{
      "skill": "missing requirement",
      "why_it_matters": "Why it matters for this role.",
      "what_to_learn": ["Topic 1", "Topic 2"],
      "practical_exercise": "A small practical project or exercise.",
      "resume_evidence": "How to demonstrate it on a resume after genuinely learning it."
    }}
  ]
}}

Do not claim the candidate already possesses missing skills.
"""

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a concise career-development assistant. "
                        "Return JSON only."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=1800,
            response_format={"type": "json_object"},
        )

        payload = _extract_json(response.choices[0].message.content)
        items = payload.get("recommendations", [])

        if not isinstance(items, list):
            raise ValueError("Invalid recommendations format returned by Groq.")

        return {"items": items, "error": None}

    except Exception as error:
        return {
            "items": [],
            "error": (
                "Groq recommendation request failed: "
                f"{type(error).__name__}: {error}"
            ),
        }