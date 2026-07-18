---
date: 2026-07-18
type: data_schema
source: [[raw/data_customers.csv]]
tags: [data-schema, customer-master]
---

# Data Customers Schema

원본: [[raw/data_customers.csv]]
행 수: 500명 (customer_id 1건당 고객 1명)

## 설명
고객 마스터 데이터입니다. 인구통계 정보(나이/성별/지역)와 가입 요금제, 해지 여부가 포함되어 있습니다.

## 컬럼
- `customer_id`: 고객 고유 ID (C001 형식)
- `name`: 고객 이름
- `age`: 나이
- `gender`: 성별 (남/여)
- `region`: 거주 지역 (서울/경기/부산/대구/인천/기타)
- `plan`: 가입 요금제 (베이직/스탠다드/프리미엄)
- `join_date`: 가입 날짜
- `churn_yn`: 해지 여부 (Y=해지, N=이용중)
- `churn_date`: 해지 날짜 (미해지 시 공란)

## 연결
- 공통 컬럼 `customer_id`로 `data_consultations`, `data_satisfaction`, `data_usage_history`, `data_voc`와 연결됩니다.

## 참고
- 이전 세션(2026-07-11)의 `customers_schema.md`는 다른 컬럼 구조(email, subscription_tier 등)를 가진 예전 placeholder 데이터 기준이었습니다. 실제 raw 데이터와 맞지 않아 삭제하고 이 노트로 대체했습니다.
