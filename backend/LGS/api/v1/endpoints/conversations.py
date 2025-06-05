from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from LGS.services.gpt_service import generate_response, chat_with_persona
from LGS.db.models.uploaded_conversation import UploadedConversations
from LGS.db.models.analyzed_conversation import AnalyzedConversations
from LGS.db.models.deleted_conversation import DeletedConversations
from LGS.schemas.uploaded_conversations import UploadedConversationOut
from LGS.db.models.persona import AIPersona
from LGS.db.session import SessionLocal



router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class ReplyRequest(BaseModel):
    user_reply: str
    use_last_analysis: bool = True  # 필요 시 마지막 대화 분석 내용까지 포함

@router.post("/conversations/upload")
async def upload_conversation(
    persona_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):  
    content = await file.read()

    persona = db.query(AIPersona).filter(AIPersona.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found.")

    new_convo = UploadedConversations(
        persona_id=persona_id,
        content=content.decode("utf-8")
    )
    db.add(new_convo)
    db.commit()
    db.refresh(new_convo)

    return {"id": new_convo.id, "created_at": new_convo.created_at}

@router.post("/conversations/reply/{persona_id}")
async def continue_reply(persona_id: int, req: ReplyRequest, db: Session = Depends(get_db)):
    persona = db.query(AIPersona).filter(AIPersona.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found.")

    convo = (
        db.query(UploadedConversations)
        .filter(UploadedConversations.persona_id == persona_id)
        .order_by(UploadedConversations.created_at.desc())
        .first()
    )
    if not convo:
        raise HTTPException(status_code=404, detail="No uploaded conversation found.")

    base_prompt = f"""
상대방은 {persona.age}살이고, 당신과의 관계는 {persona.relationship_type}입니다.
상대방의 성격: {persona.personality_summary}

다음은 최근 대화입니다:
{convo.content[:2000]}
상대방의 마지막 대답을 통해 대화의 흐름을 이어가세요.
호감을 얻기 위한 자연스럽고 효과적인 다음 한 마디를 제안해주세요.
"""
#호감 대화법: {persona.affection_prompt}

    response = generate_response(base_prompt)

    return {"reply_suggestion": response}

@router.get("/conversations/{conversation_id}", response_model=UploadedConversationOut)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = db.query(UploadedConversations).filter(UploadedConversations.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


# --- Analyzed Conversations ---
# @router.post("/conversations/analyze/", response_model=AnalyzedConversations.AnalyzedConversationsOut)
# def analyze_conversation(analyze_data: AnalyzedConversations.AnalyzedConversationsCreate, db: Session = Depends(get_db)):
#     analysis_result = analyze_conversation_service(analyze_data.query)
#     db_analysis = AnalyzedConversations(
#         uploaded_conversation_id=analyze_data.uploaded_conversation_id,
#         query=analyze_data.query,
#         response=analysis_result
#     )
#     db.add(db_analysis)
#     db.commit()
#     db.refresh(db_analysis)
#     return db_analysis


# # --- Deleted Conversations ---
# @router.post("/conversations/delete/", response_model=DeletedConversations.DeletedConversationsOut)
# def delete_conversation(delete_data: DeletedConversations.DeletedConversationsCreate, db: Session = Depends(get_db)):
#     # Fetch the uploaded conversation
#     conversation = db.query(UploadedConversations).filter(UploadedConversations.id == delete_data.uploaded_conversation_id).first()
#     if not conversation:
#         raise HTTPException(status_code=404, detail="Conversation not found")
#
#     # Mark as inactive
#     conversation.is_active = False
#     conversation.expiration_date = datetime.utcnow() + timedelta(days=7)
#     db.commit()
#
#     # Create a deletion record
#     db_deleted = DeletedConversations(**delete_data.dict())
#     db.add(db_deleted)
#     db.commit()
#     db.refresh(db_deleted)
#     return db_deleted
