from typing import Optional, List
from pydantic import BaseModel, Field


class SkillItem(BaseModel):
    canonical_name: str = Field(..., description="Normalized canonical skill identifier")
    raw_name: str = Field(..., description="Surface form matched in document text")
    category: str = Field("General", description="Category: Languages, Frameworks, Cloud, ML, Tools, etc.")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Extraction confidence score")
    evidence_snippet: Optional[str] = Field(None, description="Contextual passage where skill was identified")


class ExperienceItem(BaseModel):
    role: str = Field("Software Engineer", description="Job title or role")
    company: Optional[str] = Field(None, description="Company or organization name")
    start_date: Optional[str] = Field(None, description="Start date text")
    end_date: Optional[str] = Field(None, description="End date text or Present")
    duration_years: float = Field(0.0, ge=0.0, description="Calculated duration in years")
    description: str = Field("", description="Raw bullet points or role description")
    matched_skills: List[str] = Field(default_factory=list, description="Skills demonstrated in this role")
    snippet: Optional[str] = Field(None, description="Verbatim snippet for recruiter verification")


class EducationItem(BaseModel):
    degree: str = Field("Degree", description="Degree earned e.g. B.S., M.S., B.Tech")
    institution: Optional[str] = Field(None, description="University or college name")
    field_of_study: Optional[str] = Field(None, description="Major e.g. Computer Science")
    graduation_year: Optional[int] = Field(None, description="Year of graduation")
    gpa: Optional[str] = Field(None, description="Reported GPA or grade if present")
    snippet: Optional[str] = Field(None, description="Original source excerpt")


class ProjectItem(BaseModel):
    title: str = Field(..., description="Project name or headline")
    description: str = Field("", description="Project details, problem solved, impact")
    technologies: List[str] = Field(default_factory=list, description="Associated technologies and tools")
    snippet: Optional[str] = Field(None, description="Snippet for evidence citation")


class CertificationItem(BaseModel):
    name: str = Field(..., description="Certification name e.g. AWS Solutions Architect")
    issuing_org: Optional[str] = Field(None, description="Issuing organization e.g. Amazon, Google")
    year: Optional[int] = Field(None, description="Year acquired")
    snippet: Optional[str] = Field(None, description="Source snippet")


class ResumeParsedData(BaseModel):
    resume_id: str = Field(..., description="Unique UUID identifier for this parsed resume")
    filename: str = Field(..., description="Original filename uploaded")
    file_type: str = Field(..., description="pdf, docx, or txt")
    candidate_name: str = Field("Candidate", description="Extracted candidate name (anonymizable)")
    email: Optional[str] = Field(None, description="Contact email if found")
    phone: Optional[str] = Field(None, description="Contact phone if found")
    word_count: int = Field(0, description="Total word count in resume")
    raw_text: str = Field("", description="Extracted plain text")
    skills: List[SkillItem] = Field(default_factory=list, description="Extracted and normalized skills")
    total_experience_years: float = Field(0.0, description="Aggregate calculated work experience")
    experience: List[ExperienceItem] = Field(default_factory=list, description="Chronological work experiences")
    education: List[EducationItem] = Field(default_factory=list, description="Educational background")
    projects: List[ProjectItem] = Field(default_factory=list, description="Notable personal/work projects")
    certifications: List[CertificationItem] = Field(default_factory=list, description="Certifications")
    summary: Optional[str] = Field(None, description="Executive summary or objective")
    parsing_warnings: List[str] = Field(default_factory=list, description="Warnings e.g. potential scan, unparsed dates")
