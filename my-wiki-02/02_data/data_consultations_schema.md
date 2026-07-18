---
date: 2026-07-18
type: data_schema
source: [[raw/data_consultations.csv]]
tags: [data-schema, consultation, 재문의율]
---

# Data Consultations Schema

원본: [[raw/data_consultations.csv]]
행 수: 1,320건

## 설명
고객센터 상담 로그입니다. 상담 채널, 문의 유형, 처리 상태와 함께 **재문의 여부(is_recontact)를 직접 담고 있는 컬럼**이 있어, 재문의율 분석에 바로 사용할 수 있습니다.

## 컬럼
- `consult_id`: 상담 고유 ID (CON0001 형식)
- `customer_id`: 고객 고유 ID
- `consult_date`: 상담 발생 날짜
- `channel`: 상담 채널 (전화/채팅/앱/이메일)
- `category`: 문의 유형 (요금문의/장애신고/해지문의/명의변경/부가서비스/기타)
- `duration_min`: 상담 소요 시간(분)
- `status`: 처리 상태 (완료/미해결/재문의)
- `is_recontact`: 재문의 여부 (Y/N) — 재문의율 계산에 사용하는 핵심 필드
- `agent_id`: 담당 상담원 ID

## 연결
- `customer_id`로 고객 마스터(`[[data_customers_schema]]`)와 연결됩니다.
- `consult_id`로 만족도 데이터(`[[data_satisfaction_schema]]`)와 연결됩니다.

## 참고
- 파일명이 원래 `data_consultations (1).csv`(중복 다운로드 흔적)였으나 `data_consultations.csv`로 정리했습니다.
- 이전 세션에서는 이 파일이 `support_tickets.csv`라는 이름의 다른 컬럼 구조 데이터로 잘못 대응되어 있었고, 재문의 지표가 없다고 기록돼 있었습니다. 실제로는 `is_recontact` 컬럼이 존재하므로 해당 기록은 더 이상 유효하지 않습니다. (`[[../04_insights/insight_01_recontact_data_gap]]` 참고)
