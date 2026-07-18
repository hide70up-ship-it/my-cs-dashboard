---
date: 2026-07-11
type: data_schema
source: [[raw/feedback.csv]]
tags: [data-schema, feedback]
---

# Feedback Schema

원본: [[raw/feedback.csv]]

## 설명
고객 피드백과 만족도 정보를 기록한 데이터입니다.

## 컬럼
- `feedback_id`: 피드백 고유 ID
- `customer_id`: 고객 고유 ID
- `feedback_date`: 피드백 작성 일자
- `rating`: 만족도 점수
- `comments`: 자유 응답 코멘트

## 연결
- `customer_id`로 고객 마스터(`[[customers_schema]]`)와 연결됩니다.
