---
date: 2026-07-18
type: data_schema
source: [[raw/data_usage_history.csv]]
tags: [data-schema, 이용이력, usage]
---

# Data Usage History Schema

원본: [[raw/data_usage_history.csv]]
행 수: 6,000건 (고객 1명당 월별 1행, 2024년 1월~12월)

## 설명
고객별 월간 서비스 이용 내역입니다. 데이터 사용량, 통화량, 청구 금액, 부가서비스/앱 이용 빈도가 포함됩니다.

## 컬럼
- `usage_id`: 이용기록 고유 ID
- `customer_id`: 고객 고유 ID
- `year_month`: 대상 연월 (예: 2024-01)
- `data_gb`: 해당 월 데이터 사용량(GB)
- `call_min`: 해당 월 통화 시간(분)
- `billing_amount`: 해당 월 청구 금액(원)
- `service_count`: 해당 월 이용한 부가서비스 개수
- `app_login_count`: 해당 월 앱 로그인 횟수

## 연결
- `customer_id`로 고객 마스터(`[[data_customers_schema]]`)와 연결됩니다.

## 참고
- 이전 세션의 `usage_logs_schema.md`(log_id, service_used 등 다른 컬럼 구조)는 이 데이터와 대응되지 않아 삭제하고 이 노트로 대체했습니다.
