from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from LGS.core.security import decode_access_token
from LGS.db.session import SessionLocal
from LGS.db.models.user import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(Authorization: str = Header(...), db: Session = Depends(get_db)) -> User:
    token = Authorization.replace("Bearer ", "")
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다.")
    return user
