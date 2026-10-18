# 단단이 V0.5.2 — 아침 알림 설정 및 미리보기

V0.5.1에서 검증한 11장 이미지, 3열 사진 카드, 해설, 창조형 하루 기능을 유지합니다.

## 이번 버전
- 기본 꺼짐의 알림 희망 설정
- 한국 시간 기준 30분 간격 시각 선택, 매일/주 3회/주 1회, 요일, 주제 선택
- 설정 검증, 저장 상태 표시, 언제든 끄기
- 선택 주제의 문장 미리보기 및 해설 확인

**실제 예약 알림/푸시 발송은 구현되지 않았습니다.** Colab의 로컬 JSON 설정은 세션 종료 시 유실될 수 있습니다. 앱을 공개 배포할 때는 사용자별 계정/저장소 분리, 동의, 푸시 권한, 스케줄러, 보안 설정이 필요합니다.

## Colab
`pip install -r requirements.txt` 후 `streamlit run app.py --server.port=8513 --server.address=127.0.0.1 --server.headless=true`
Colab 포트 iframe에서 WebSocket Origin/Host 거절이 발생하는 경우에만 개인 테스트 환경에서 `--server.enableCORS=false --server.enableXsrfProtection=false` 옵션을 임시 사용합니다. 공개 서비스에는 사용하지 않습니다.
