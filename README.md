# 단단이 V0.4.1 — 사진형 카테고리 대시보드

V0.4를 기반으로 독립 복제한 버전입니다. 기존 프로젝트는 수정하지 않습니다.

## 추가 기능
- 주제별 시네마틱 사진 카드 대시보드
- 사진 아래 탐색 버튼을 눌러 해당 주제 문장/해설로 연결
- 희망 이미지와 신학 이미지를 분리
- 기존 보관함·다짐·알림 설정 유지

## Colab
`pip install -r /content/dandani_v041/requirements.txt`
`streamlit run /content/dandani_v041/app.py --server.port 8508 --server.address 127.0.0.1 --server.headless true`

## 주의
저장 데이터는 현재 앱 폴더의 JSON에 저장됩니다. Colab 초기화 시 소실될 수 있고 여러 사용자 간 분리되지 않으므로 공개 서비스용이 아닙니다. 실제 푸시 알림도 아직 지원하지 않습니다.
