---
date: 2026-07-11
type: question
stage: 예측적
related_data:
  - [[02_data/customers_schema]]
  - [[02_data/support_tickets_schema]]
  - [[02_data/feedback_schema]]
  - [[02_data/usage_logs_schema]]
tags: [예측적, 이탈예측, 재문의율]
---

# 고객 CS 기반 이탈 예측

- 어떤 고객이 향후 재문의나 이탈 가능성이 높은가?
- 상담 이력과 만족도 데이터를 통해 재문의/이탈 위험군을 예측합니다.

## 필요 데이터
- `customers` 고객 마스터
- `support_tickets` 상담 로그
- `feedback` 피드백 데이터
- `usage_logs` 이용 이력
