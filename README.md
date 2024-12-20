# 로컬 실행

```bash
uvicorn "src.app_module:http_server" --host "0.0.0.0" --port "8080" --reload
```
# 정렬

poetry run black src/                                                                                                     
poetry run pyright src/
poetry run isort src/
poetry run flake8 src/
poetry run refurb src/

## 문제점 및 트러블 슈팅
- 기존에 질문만 임베딩 하려 했으나, 답변도 함께 임베딩 해야함
- 질답을 한번에 임베딩 하려니 토큰 길이가 너무 길어짐
- 슬라이딩 윈도우 방식으로 토큰 길이를 줄이려 했으나, 문장의 중요한 정보가 잘리는 문제 발생
- 각각 겹치는 부분을 생기도록 하여 정보 손실을 최소화

해당 기능의 장점
- 사용자 경험 개선:
  한 번에 긴 답변을 주기보다 단계별로 정보를 제공
- 맥락 유지:
  사용자가 질문을 하는 과정에서 추가적인 정보나 맥락
- 응답 최적화:
  질문을 여러 단계로 나눠 처리하면 더 짧고 정확한 정보를 제공

### 히스토리 기능 Max Token 제한
- 히스토리가 길어질수록 토큰 길이가 길어짐 - 비용 , 성능 저하 및 에러 발생
- 히스토리를 제한하여 토큰 길이를 줄임 최대 5개 까지만 요청에 재사용

### LLM 답변이 짧을 경우 응답 연관성 문제
- LLM 응답이 짧을 경우, 질문에 대한 연관성이 떨어짐
- 사용한 검색증강 데이터를 LLM에게 추가 하는 방식이 필요 하다고 생각되나 steraming 방식으로는 불가능 해보임
- 이전 질문에 캐싱한 사용자 텍스트 임베딩 데이터를 통해 사용한 RAG 데이터를 추가하여 연관성을 높히는게 필요해 보임
- 또는 이전 질/답을 함께 텍스트 임베딩 하는 것도 괜찮은 방법으로 보이나 해당 문제도 토큰 길이 문제가 발생함 그러나 생각보다 길지 않아 보임 많이 길어질 경우 텍스트 요약 모델을 사용하는 것이 좋아보임
- 문제로 이전 답변 내용과 다른 질문을 한 경우 연관성이 떨어질 수 있음 이경우 이전 답변의 텍스트 임베딩 또한 함께 사용하여 연관성을 높히는 방법이 필요해 보임
- 상기 기법으로 이전 답변에 종속적인 답변을 제공 하게됨 -> LLM 히스토리 요청 방식을 변경 

## 프로젝트 구조 
```
src/
├── __init__.py
├── app_controller.py
├── app_module.py
├── app_service.py
├── config/
│   ├── __init__.py
│   └── env_variable.py
└── domain/
    ├── __init__.py
    ├── base/
    │   ├── __init__.py
    │   └── pydantic_base.py
    ├── faq/
    │   ├── __init__.py
    │   ├── faq_controller.py
    │   ├── faq_module.py
    │   ├── faq_search_repository.py
    │   ├── faq_service.py
    │   ├── question.py
    │   └── question_history_repository.py
    ├── llm/
    │   ├── __init__.py
    │   ├── open_ai_client.py
    │   ├── open_ai_module.py
    │   └── prompt/
    │       ├── __init__.py
    │       └── question_promt.py
    └── milvus/
        ├── __init__.py
        ├── milvus_module.py
        └── milvus_search_client.py

```