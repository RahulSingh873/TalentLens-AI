import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse

from .config import settings
from .api.resumes import router as resumes_router
from .api.jobs import router as jobs_router
from .api.match import router as match_router
from .api.recommendations import router as recommendations_router
from .api.evaluation import router as evaluation_router
from .nlp.embeddings import embedding_engine

app = FastAPI(
    title=settings.app_name,
    description="Explainable, AI-Powered Resume Screening and Candidate Recommendation System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(resumes_router)
app.include_router(jobs_router)
app.include_router(match_router)
app.include_router(recommendations_router)
app.include_router(evaluation_router)


@app.get("/api/health")
def health_check():
    """Health check and model runtime status."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "environment": settings.app_env,
        "embedding_model": embedding_engine.model_name,
        "device": settings.embedding_device,
        "active_resumes_count": len(resumes_router.routes),
    }


# Serve standalone dashboard UI if index.html exists in frontend/dist or frontend/
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

if os.path.exists(frontend_dist) and os.path.exists(os.path.join(frontend_dist, "index.html")):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_react_app(full_path: str):
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return None
        return FileResponse(os.path.join(frontend_dist, "index.html"))

elif os.path.exists(os.path.join(frontend_dir, "index.html")):
    @app.get("/")
    def serve_frontend_root():
        return FileResponse(os.path.join(frontend_dir, "index.html"))

else:
    @app.get("/")
    def serve_fallback_welcome():
        return HTMLResponse(
            """
            <html>
                <head><title>TalentLens AI</title></head>
                <body style="font-family: sans-serif; padding: 40px; text-align: center;">
                    <h1>TalentLens AI Backend Running</h1>
                    <p>API Documentation available at <a href="/docs">/docs</a></p>
                </body>
            </html>
            """
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.host, port=settings.port, reload=True)
