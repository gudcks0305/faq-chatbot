# 코드 결과물 
```
src/ 디렉토리에 핵심 코드가 포함되어 있습니다.
Poetry 기반 환경에서 실행 가능하도록 pyproject.toml 및 requirements.txt(또는 poetry.lock)를 포함하였습니다.
```

# 문제 접근 방법
## embdding 전략:
- 사용한 개발 기술들이 처음 사용하는 것들이라 P.O.C 단계를 거쳐서 사용하였습니다.
- jupyter notebook을 사용하여 데이터를 확인하고, 데이터를 가공하여 사용하였습니다.

## 질의응답 임베딩 전략:
### 해결 접근 순서 
1. 문제 - 질문만 임베딩하려 했으나, 연관 질문 대응을 위해 답변도 함께 임베딩해야 함
2. 문제 - 질답을 한 번에 임베딩하려니 토큰 길이가 너무 길어져 토큰 제한에 걸림
3. 문제 - 슬라이딩 윈도우 방식으로 토큰 길이를 줄이려 했으나, 문장의 중요한 정보가 잘리는 문제 발생하여 결과가 부정확함
### 결과 
- 질문(Query)뿐만 아니라 답변(Answer)도 함께 임베딩하여 맥락성을 유지했습니다.
- 토큰 길이 관리 문제로 긴 Q&A를 한 번에 임베딩하기 어려운 경우, 슬라이딩 윈도우 방식에 겹치는 부분을 두어 정보 손실을 최소화했습니다. 추가적으로 원본 데이터를 로우에 저장하여 LLM 요청 시 해당 데이터를 사용할 수 있게 했습니다.

## 맥락 유지 전략:
- 긴 답변을 단계적으로 나누어 제공하여 사용자의 경험을 개선합니다.
- 히스토리를 최대 5개까지만 유지하여 토큰 비용 및 성능 문제를 완화 하였습니다.

## 응답 품질 개선 시도:
- 답변 길이가 너무 짧을 경우 관련성이 떨어질 수 있으므로, 답변을 vector embedding로 임베딩하고, LLM 응답 시에 반영하는 방식을 모색하였습니다.
- 이전 질문/답변을 함께 임베딩하거나, 필요할 경우 요약 모델을 통해 토큰 길이를 줄이는 전략을 적용할 수 있습니다.
- openai LLM interface의 List 형식 히스토리를 사용 하려 했으나 이전 답변에 종속적인 답변을 제공하게 되어 문제가 발생하여 하나의 요청 내부에 이전 답변을 포함하여 요청하는 방식으로 변경하였습니다.

## LLM 모델 선택 이유:
- https://artificialanalysis.ai/leaderboards/models 에서 LLM 모델을 비교하여 선택하였습니다. 
- 성능 대비 비용이 저렴 하고 chatbot에 적합한 모델로 판단하였습니다. (gpt4o-mini)

## 코드 결과물 설명
주요 모듈 (src/ 디렉토리)
- app_module.py: FastAPI - Pynest 기반 http_server 구동 및 라우팅 설정
- domain/faq/faq_service.py: FAQ 관련 질의응답 로직 처리
- domain/faq/faq_search_repository.py: FAQ 검색 로직 milvus client를 wrapper한 클래스
- domain/faq/question_history_repository.py: 질문 히스토리 관리 로직 처리 in-memory 형식으로 구현
- domain/llm/open_ai_client.py: OpenAI API 연동 로직
- domain/milvus/milvus_search_client.py: 벡터 데이터베이스(Milvus) 연결 검색 로직
- config/env_variable.py: 환경변수 관리

일반적인 Java - Spring Boot 기반의 프로젝트 구조와 유사하게 구성하였습니다. ( DI 및 계층 구조 적용 ) 

## 실행 방법 
```bash
cat <<EOF > .env
OPEN_API_KEY={YOUR_API_KEY}
EOF

uvicorn "src.app_module:http_server" --host "0.0.0.0" --port "8080" --reload
```

## 데모 시나리오 

### 중간 중간 스마트 스토어와 관련 없는 질문을 하는 경우
- q1 : 미성년자도 판매회원으로 가입할 수 있나요?
  - a1 : {답변}
- q2 : 아 오늘 날씨가 정말 좋네요
  - a2 : 스마트스토어 FAQ를 위한 챗봇입니다. 스마트스토어 관련 질문을 부탁드립니다.
- q3 : 가입에 필요한 서류는 무엇인가요?
  - a3 : {답변}
- 
```bash
curl -X 'POST' \
  'http://localhost:8080/api/v1/faqs/question/stream' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "미성년자도 판매회원으로 가입할 수 있나요?"
}'

curl -X 'POST' \
  'http://localhost:8080/api/v1/faqs/question/stream' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "아 오늘 날씨가 정말 좋네요"
}'
curl -X 'POST' \
  'http://localhost:8080/api/v1/faqs/question/stream' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "가입에 필요한 서류는 무엇인가요?"
}'


```
### 스마트 스토어와 관련된 질문을 하는 경우에 이전 질문과 관련 없는 질문을 하는 경우
```bash
curl -X 'POST' \
  'http://localhost:8080/api/v1/faqs/question/stream' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "적발로 인한 과태료 부과 시 스토어(쇼핑몰)에서 차감되나요?"
}'
```

## 아쉬운 점
- 원본 데이터를 정규화하여 마스터 컬랙션으로 저장 할 수 있었을 텐데 api 숙련도 문제로 구현 하지 못한 점
- milvus api 가 async 를 지원하지 않아서 비동기 처리를 하지 못한 점 
