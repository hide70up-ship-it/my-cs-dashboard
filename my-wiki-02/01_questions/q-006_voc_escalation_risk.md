---
date: 2026-07-11
type: question
stage: 예측적
related_data:
  - [[02_data/voc_schema]]
  - [[02_data/support_tickets_schema]]
  - [[02_data/feedback_schema]]
tags: [예측적, VOC, 위험예측]
---

# VOC 기반 상담 악화 위험 예측

- 어떤 VOC 유형이 이후 상담 악화 또는 재문의로 이어질 가능성이 높은가?
- VOC와 상담 상태 변화를 기반으로 문제 심각도 위험을 예측합니다.

## 필요 데이터
- `voc` VOC 데이터
- `support_tickets` 상담 로그
- `feedback` 피드백 데이터
