---
date: 2026-07-18
type: data_schema
source: [[raw/data_voc.csv]]
tags: [data-schema, VOC, sentiment]
---

# Data VOC Schema

원본: [[raw/data_voc.csv]]
행 수: 1,307건

## 설명
고객의 소리(Voice of Customer) 데이터입니다. 상담 채널과 별개로 앱리뷰, SNS, 이메일, 고객센터전화 등을 통해 접수된 의견/불만/제안/칭찬을 담고 있으며, 감정 분석 결과(sentiment)가 포함됩니다.

## 컬럼
- `voc_id`: VOC 고유 ID (V0001 형식)
- `customer_id`: 고객 고유 ID
- `received_date`: 접수 날짜
- `channel`: 접수 채널 (고객센터전화/앱리뷰/이메일/SNS)
- `voc_type`: VOC 성격 (불만/문의/제안/칭찬)
- `category`: 주제 (요금/품질/서비스/앱기능/해지관련/기타)
- `content`: 원문 내용
- `sentiment`: 감정 분석 결과 (긍정/중립/부정)

## 연결
- `customer_id`로 고객 마스터(`[[data_customers_schema]]`)와 연결됩니다.

## 참고
- 이전 세션에서 질문(`q-002`, `q-006`, `q-008`)이 참조하던 `[[02_data/voc_schema]]`는 실제로 생성된 적이 없었습니다. 이 노트가 그 자리를 채웁니다.
