from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from LGS.db.session import SessionLocal
from LGS.schemas.persona import AIPersonaCreate, AIPersonaOut
from LGS.db.models.persona import AIPersona
from LGS.core.security import hash_password
from LGS.services.gpt_service import summarize_personality
from LGS.dependencies import get_current_user
from LGS.db.models.user import User
from typing import List
import os
from uuid import uuid4

UPLOAD_DIR = "uploads/profiles"
DEFAULT_PROFILE = "/uploads/profiles/default-profile.png"  # ✅ 기본 이미지 경로 (FastAPI가 제공하는 static path 기준)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/upload", response_model=AIPersonaOut)
async def upload_persona_file(
    name: str = Form(...),
    mbti: str = Form(None),
    file: UploadFile = File(...),
    profile: UploadFile = File(None),  # ✅ 이미지 파일 (선택)
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 텍스트 읽기
    contents = await file.read()
    text = contents.decode("utf-8")
    summary_output = summarize_personality(text)
    
    profile_url = DEFAULT_PROFILE  # 기본값으로 설정해두고
    if profile:
        ext = os.path.splitext(profile.filename)[1]
        filename = f"{uuid4().hex}{ext}"
        save_path = os.path.join(UPLOAD_DIR, filename)
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(await profile.read())
        profile_url = f"/{save_path}"

    persona = AIPersona(
        name=name,
        mbti=mbti,
        personality_summary=summary_output,
        user_id=current_user.id,
        profile_url=profile_url
    )
    db.add(persona)
    db.commit()
    db.refresh(persona)
    return persona

@router.get("/list", response_model=List[AIPersonaOut])
def list_personas(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    personas = db.query(AIPersona).filter(AIPersona.user_id == current_user.id).order_by(AIPersona.created_at.desc()).all()
    for persona in personas:
        print(persona.__dict__)
    
    return personas