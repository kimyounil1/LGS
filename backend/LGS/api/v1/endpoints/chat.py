from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from LGS.db.session import SessionLocal
from LGS.db.models.message import Message
from LGS.db.models.persona import AIPersona
from LGS.schemas.message import MessageCreate, MessageOut
from LGS.services.gpt_service import chat_with_persona
from typing import List
from LGS.dependencies import get_current_user
from LGS.db.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send", response_model=List[MessageOut])
def send_message(data: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 캐릭터 존재 확인
    persona = db.query(AIPersona).filter(
        AIPersona.id == data.persona_id, #data.persona_id가 안타고 온다 수정해야함함
        AIPersona.user_id == current_user.id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="AI 캐릭터를 찾을 수 없습니다.")

    # 1. 유저 메시지 저장
    user_msg = Message(
        persona_id=data.persona_id,
        sender="user",
        content=data.content,
    )
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # 2. 최근 메시지 몇 개 불러오기
    history = db.query(Message)\
        .filter(Message.persona_id == data.persona_id)\
        .order_by(Message.created_at.desc())\
        .limit(10).all()

    history = list(reversed(history))  # 시간순 정렬

    # 3. GPT 응답 생성
    ai_response = chat_with_persona(persona, history)

    # 4. GPT 응답 저장
    ai_msg = Message(
        persona_id=data.persona_id,
        sender="ai",
        content=ai_response,
    )
    db.add(ai_msg)
    db.commit()
    db.refresh(ai_msg)

    return [user_msg, ai_msg]

@router.get("/history", response_model=List[MessageOut])
def get_chat_history(
    persona_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 권한 확인: 내 캐릭터인지
    persona = db.query(AIPersona).filter(
        AIPersona.id == persona_id,
        AIPersona.user_id == current_user.id
    ).first()

    if not persona:
        raise HTTPException(status_code=404, detail="캐릭터가 없거나 권한 없음")

    messages = db.query(Message).filter(
        Message.persona_id == persona_id
    ).order_by(Message.created_at).all()

    return messages
