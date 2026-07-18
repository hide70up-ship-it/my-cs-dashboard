---
date: 2026-07-18
confidence: 높음
source_data:
  - [[raw/data_consultations.csv]]
source_question:
  - [[01_questions/q-003_recontact_patterns]]
tags: [재문의율, 채널효율, 갱신됨]
status: 해소됨 (2026-07-18)
---

# 채널별 재문의율 분석 준비 현황

## 근거
(2026-07-11 최초 작성 시) 당시 raw 데이터 폴더에는 `support_tickets.csv`가 있었으나 재문의 여부를 나타내는 컬럼이 없어, 재문의율 분석이 불가능하다고 판단했었습니다.

(2026-07-18 갱신) 이후 `raw/data_consultations.csv`가 새로 추가되었고, 이 파일에는 `is_recontact`(Y/N) 컬럼이 이미 포함되어 있습니다. 또한 `status` 컬럼에도 '재문의'라는 상태값이 별도로 존재합니다.

## 해석
- 이전에 지적했던 "재문의 지표 부재" 문제는 더 이상 유효하지 않은 것으로 보입니다.
- `is_recontact` 컬럼을 `channel`, `category`별로 집계하면 채널별·문의유형별 재문의율을 바로 계산할 수 있는 상태입니다 (가설: 실제 집계는 아직 수행하지 않음).
- `status`의 '재문의' 값과 `is_recontact`의 'Y' 값이 서로 일치하는지도 교차 확인이 필요합니다 (가설: 두 필드가 동일 개념을 이중으로 기록했을 가능성).

## 시사점
- 이전에 `00_inbox/inbox_01_raw_data_presence`, `inbox_02_recontact_metric_review`에 남겨둔 "데이터 부족" 검토 요청은 해소된 것으로 볼 수 있습니다. 다만 이 두 인박스 노트는 아직 원문 그대로 남아 있으니, 별도로 정리(archiving)가 필요합니다.
- 다음 단계로 `03_analysis/`에 실제 재문의율 집계(채널별/문의유형별 `is_recontact` 비율)를 계산하는 분석 기록을 작성하는 것을 추천합니다.
- CLAUDE.md 기준(재문의율 20% 이상 = 개선 필요)에 맞춰 세그먼트별 임계치 초과 여부를 확인해야 합니다.
