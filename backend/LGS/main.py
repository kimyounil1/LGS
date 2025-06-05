from fastapi import FastAPI
<<<<<<< HEAD
from LGS.api.v1.endpoints import auth, persona, chat, conversations, forecast
=======
from LGS.api.v1.endpoints import auth, persona, chat
>>>>>>> origin/master
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
#아래는 초기값 설정
from LGS.db.session import engine
from LGS.db.models import user
from LGS.db.base_class import Base
app = FastAPI()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#아래는 DB 초기화 (초기만 사용)
def init_db():
    Base.metadata.create_all(bind=engine)

# FastAPI 실행 시 호출
init_db()

# 파일 업로드 경로

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# API 경로

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(persona.router, prefix="/api/v1/persona", tags=["Persona"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
<<<<<<< HEAD
app.include_router(conversations.router, prefix="/api/v1/conversations", tags=["Conversations"])
app.include_router(forecast.router, prefix="/api/v1/forecast", tags=["Forecast"])

=======
>>>>>>> origin/master
