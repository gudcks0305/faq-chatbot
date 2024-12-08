# 로컬 실행 

```bash
uvicorn "src.app_module:http_server" --host "0.0.0.0" --port "8080" --reload
```
# 정렬 

poetry run black app/                                                                                                     
poetry run pyright app/
poetry run isort app/
poetry run flake8 app/
poetry run refurb app/

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