---
date: 2026-07-18
type: data_schema
source: [[raw/data_satisfaction.csv]]
tags: [data-schema, 만족도, csat, nps]
---

# Data Satisfaction Schema

원본: [[raw/data_satisfaction.csv]]
행 수: 1,320건 (상담 1건당 만족도 조사 1건)

## 설명
상담 직후 진행한 만족도 조사 데이터입니다. CSAT(만족도 점수)와 NPS(추천 의향 점수), 자유 코멘트가 포함됩니다.

## 컬럼
- `satisfaction_id`: 설문 고유 ID (SAT0001 형식)
- `consult_id`: 어느 상담에 대한 조사인지 (`data_consultations`와 연결)
- `customer_id`: 고객 고유 ID
- `survey_date`: 조사 날짜
- `csat`: 만족도 점수 (1~5점, 높을수록 만족)
- `nps`: 추천 의향 점수 (0~10점, 높을수록 추천 의향 큼)
- `comment`: 자유 응답 코멘트 (공란 가능)

## 연결
- `consult_id`로 상담 로그(`[[data_consultations_schema]]`)와 1:1 연결됩니다.
- `customer_id`로 고객 마스터(`[[data_customers_schema]]`)와 연결됩니다.

## 참고
- 이전 세션의 `feedback_schema.md`(다른 컬럼 구조: feedback_id, rating 등)는 이 데이터와 대응되지 않아 삭제하고 이 노트로 대체했습니다.
