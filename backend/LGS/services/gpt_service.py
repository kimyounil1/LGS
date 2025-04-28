# 1. 'OpenAI' 클래스를 직접 임포트합니다.
from openai import OpenAI
from LGS.core.config import settings # 설정 파일은 그대로 사용합니다.

# 2. OpenAI 클라이언트 객체를 생성하고 API 키를 전달합니다.
#    이전처럼 openai.api_key = ... 로 설정하는 대신, 클라이언트 생성 시점에 키를 넣어줍니다.
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def summarize_personality(text: str) -> str:
    prompt = f"""
다음은 카카오톡 대화 내용입니다. 상대방의 성격을 요약해줘. MBTI 성향도 포함해서 요약해줘.

[대화 내용]
{text[:1500]}

→ 출력 형식:
- 성격 요약:
- 추정 MBTI:
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_completion_tokens=1000
    )

    return response.choices[0].message.content

def chat_with_persona(persona, history: list) -> str:
    prompt_messages = [
        {
            "role": "system",
            "content": f"너는 이제 '{persona.name}'라는 사람처럼 말해야 해. 성격은 다음과 같아:\n{persona.personality_summary}"
        }
    ]
    for msg in history:
        prompt_messages.append({
            "role": "user" if msg.sender == "user" else "assistant",
            "content": msg.content
        })

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=prompt_messages,
        temperature=0.8,
        max_completion_tokens=1000
    )

    return response.choices[0].message.content
