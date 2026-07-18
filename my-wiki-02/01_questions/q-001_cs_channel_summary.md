---
date: 2026-07-11
type: question
stage: 기술적
related_data:
  - [[02_data/customers_schema]]
  - [[02_data/support_tickets_schema]]
  - [[02_data/usage_logs_schema]]
tags: [기술적, CS채널, 상담현황]
---

# CS 채널별 상담 현황 분석

- 어떤 CS 채널에서 상담 요청이 가장 많은가?
- 채널별 상담 건수와 고객 수를 비교하여 서비스 부하를 파악합니다.

## 필요 데이터
- `support_tickets` 상담 로그
- `usage_logs` 서비스 이용 이력
- `customers` 고객 마스터
