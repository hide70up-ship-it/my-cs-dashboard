---
date: 2026-07-11
type: analysis_plan
related_question: [[01_questions/question_01_recontact_analysis]]
tags: [CS분석, 재문의율, VOC]
---

# 재문의율 및 VOC 분석 계획

## 목표
고객 재문의율과 VOC 데이터를 분석하여 재문의가 높은 서비스 채널과 주요 이슈를 파악합니다.

## 사용 데이터
- `[[02_data/customers_schema]]`
- `[[02_data/transactions_schema]]`
- `[[02_data/support_tickets_schema]]`
- `[[02_data/usage_logs_schema]]`
- `[[02_data/feedback_schema]]`

## 분석 단계
1. 고객별 `customer_id`를 기준으로 고객 정보와 상담/이용/피드백 데이터를 연결합니다.
2. `support_tickets`에서 재문의 여부가 포함된 지표를 생성합니다.
3. `feedback` 점수 및 코멘트와 재문의율을 비교 분석합니다.
4. 재문의율이 20% 이상인 세그먼트를 우선적으로 검토합니다.
5. 결과를 기반으로 인사이트 정리 노트를 `04_insights`에 작성합니다.

## 기대 결과
- 재문의율이 높은 고객 군과 서비스 유형
- VOC 이슈 우선순위
- 개선 필요 영역
