import os
from pydantic import BaseModel, Field


class ScoringWeights(BaseModel):
    required_skills: float = Field(0.40, ge=0.0, le=1.0, description="Weight for required mandatory skills")
    preferred_skills: float = Field(0.15, ge=0.0, le=1.0, description="Weight for preferred optional skills")
    semantic_similarity: float = Field(0.25, ge=0.0, le=1.0, description="Weight for dense contextual embedding similarity")
    experience: float = Field(0.15, ge=0.0, le=1.0, description="Weight for relevant work experience duration & scope")
    projects: float = Field(0.05, ge=0.0, le=1.0, description="Weight for demonstrated practical projects")

    def validate_weights(self) -> bool:
        total = self.required_skills + self.preferred_skills + self.semantic_similarity + self.experience + self.projects
        return abs(total - 1.0) < 1e-3


class AppSettings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "TalentLens AI")
    app_env: str = os.getenv("APP_ENV", "development")
    app_debug: bool = os.getenv("APP_DEBUG", "true").lower() == "true"
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    
    # Embedding configuration
    embedding_model_name: str = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
    embedding_device: str = os.getenv("MODEL_DEVICE", "cpu")
    
    # Storage & Limits
    max_upload_size_bytes: int = int(os.getenv("UPLOAD_MAX_BYTES", "10485760")) # 10MB
    allowed_file_types: list[str] = ["pdf", "docx", "txt"]
    storage_dir: str = os.getenv("DATA_DIR", "./data")
    models_dir: str = os.getenv("MODELS_DIR", "./models")
    reports_dir: str = os.getenv("REPORTS_DIR", "./reports")
    
    # Default scoring configuration
    default_weights: ScoringWeights = ScoringWeights()


settings = AppSettings()
