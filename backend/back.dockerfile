ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}-slim

WORKDIR /LGS

# 시스템 종속성 설치 (필요시)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

<<<<<<< HEAD
RUN apt-get update && apt-get install -y git

=======
>>>>>>> origin/master
# Python 종속성 설치 (캐시 효율화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# FastAPI 실행
CMD ["uvicorn", "LGS.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]