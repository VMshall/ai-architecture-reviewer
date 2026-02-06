from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.reviewer import review_architecture
import traceback

app = FastAPI(title="AI Architecture Reviewer")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class ReviewRequest(BaseModel):
    design_doc: str
    system_type: str = "web application"
    scale_requirements: str = ""


@app.post("/review")
async def review(req: ReviewRequest):
    if not req.design_doc.strip():
        raise HTTPException(400, "Design document required")
    try:
        return review_architecture(req.design_doc, req.system_type, req.scale_requirements)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, str(e))


@app.get("/health")
def health():
    return {"status": "ok"}


app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
