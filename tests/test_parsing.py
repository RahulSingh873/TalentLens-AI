import os
import tempfile
from backend.nlp.parser import segment_sections, parse_experience_section, extract_contact_info, parse_resume


def test_section_segmentation():
    sample_resume = """
John Doe
john.doe@example.com | (555) 123-4567

PROFESSIONAL SUMMARY
Senior Engineer with extensive backend experience.

WORK EXPERIENCE
Software Engineer | Acme Corp (2021 - Present)
- Built microservices using Python and Docker.

EDUCATION
B.S. in Computer Science | University of California (2020)

TECHNICAL SKILLS
Python, Docker, FastAPI, PostgreSQL
    """.strip()

    sections = segment_sections(sample_resume)
    assert "experience" in sections
    assert "education" in sections
    assert "skills" in sections
    assert "Acme Corp" in sections["experience"]
    assert "Computer Science" in sections["education"]


def test_contact_info_extraction():
    text = "Jane Smith\njane.smith@techdomain.org\nPhone: (415) 555-9876\nSan Francisco, CA"
    email, phone, name = extract_contact_info(text)
    assert email == "jane.smith@techdomain.org"
    assert phone is not None
    assert "Jane Smith" in name


def test_experience_duration_calculation():
    exp_text = "Software Engineer (2021 - Present)\nBuilt cloud infrastructure.\nJunior Developer (2019 - 2021)\nAssisted backend development."
    items, total_years = parse_experience_section(exp_text)
    assert len(items) >= 1
    assert total_years >= 2.0
