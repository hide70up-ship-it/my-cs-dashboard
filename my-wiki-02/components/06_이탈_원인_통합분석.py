import pandas as pd
from pathlib import Path

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

# 데이터 읽기
base_dir = Path(__file__).resolve().parents[1]
raw_dir = base_dir / 'raw'

customers = pd.read_csv(raw_dir / 'data_customers.csv')
consultations = pd.read_csv(raw_dir / 'data_consultations.csv')
satisfaction = pd.read_csv(raw_dir / 'data_satisfaction.csv')
usage = pd.read_csv(raw_dir / 'data_usage_history.csv')
voc = pd.read_csv(raw_dir / 'data_voc.csv')

# 1) 상담: 고객 단위 집계 (상담 건수, 재문의율, 미해결율)
consult_agg = consultations.groupby('customer_id').agg(
    consult_count=('consult_id', 'count'),
    recontact_rate=('is_recontact', lambda s: (s == 'Y').mean() * 100),
    unresolved_rate=('status', lambda s: (s == '미해결').mean() * 100),
).reset_index()

# 2) 만족도: 고객 단위 평균
satisfaction_agg = satisfaction.groupby('customer_id').agg(
    avg_csat=('csat', 'mean'),
    avg_nps=('nps', 'mean'),
).reset_index()

# 3) 이용 이력: 고객 단위 평균 + 상반기 대비 하반기 변화율 (감소 추세 확인용)
# 주의 1: 이탈 고객은 churn_date 이후에도 이용 이력 행이 남아있고 값이 0에 가깝게 찍혀 있음.
#         이걸 그대로 평균 내면 "이미 떠난 뒤의 0"이 "이탈 전 감소 신호"처럼 보이는 착시가 생김.
# 주의 2: 이탈월 자체도 한 달을 다 채우지 못한 "부분월"이라 값이 낮게 찍히므로 함께 제외해야 함.
# -> 이탈 고객은 churn_date가 속한 달의 시작일 이전(완전히 재직한 달)만 사용한다.
usage = usage.merge(customers[['customer_id', 'churn_yn', 'churn_date']], on='customer_id', how='left')
usage['year_month_ts'] = pd.to_datetime(usage['year_month'])
usage['churn_date'] = pd.to_datetime(usage['churn_date'])
usage['churn_month_start'] = usage['churn_date'].dt.to_period('M').dt.to_timestamp()
is_active_period = (usage['churn_yn'].eq('N')) | (usage['year_month_ts'] < usage['churn_month_start'])
usage_pre_churn = usage[is_active_period]

usage_avg = usage_pre_churn.groupby('customer_id').agg(
    avg_data_gb=('data_gb', 'mean'),
    avg_call_min=('call_min', 'mean'),
    avg_app_login_count=('app_login_count', 'mean'),
    active_month_count=('year_month', 'count'),
).reset_index()

usage_pre_churn = usage_pre_churn.copy()
usage_pre_churn['half'] = usage_pre_churn['year_month'].apply(lambda ym: 'H1' if ym <= '2024-06' else 'H2')
half_pivot = usage_pre_churn.groupby(['customer_id', 'half'])['data_gb'].mean().unstack('half').reset_index()
# H1/H2 둘 다 재직 중 데이터가 있는 고객만 변화율 계산 (한쪽이 없으면 비교 불가 -> NaN 유지)
half_pivot['data_gb_change_pct'] = (
    (half_pivot['H2'] - half_pivot['H1']) / half_pivot['H1'] * 100
)
usage_agg = usage_avg.merge(
    half_pivot[['customer_id', 'data_gb_change_pct']], on='customer_id', how='left'
)

# 4) VOC: 고객 단위 집계 (VOC 건수, 부정 감정 비율)
voc_agg = voc.groupby('customer_id').agg(
    voc_count=('voc_id', 'count'),
    negative_voc_rate=('sentiment', lambda s: (s == '부정').mean() * 100),
).reset_index()

# 전체 병합 (고객 마스터 기준 left join)
profile = (
    customers
    .merge(consult_agg, on='customer_id', how='left')
    .merge(satisfaction_agg, on='customer_id', how='left')
    .merge(usage_agg, on='customer_id', how='left')
    .merge(voc_agg, on='customer_id', how='left')
)

# 건수(count)는 이력이 없으면 0건이 맞으므로 그대로 채움.
# 단, 비율(rate)/평균 계열은 "이력이 아예 없음"과 "0%"가 다른 의미이므로 채우지 않고 NaN으로 남겨
# groupby 평균 계산 시 자연스럽게 제외되도록 한다 (그래야 이탈 고객군의 상담 이력 0건 비중이 높다는
# 이유만으로 재문의율 평균이 인위적으로 낮아지는 왜곡을 막을 수 있음).
for col in ['consult_count', 'voc_count']:
    profile[col] = profile[col].fillna(0)

output_dir = base_dir / 'components' / 'output'
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / '06_customers_full_profile.csv'
profile.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f'저장 완료: {output_path} (총 {len(profile)}행)')
print()

# 이탈 여부(Y/N)별 비교: 요금제와 무관하게 실제 경험 지표가 다른지 확인
print('=== 이탈 여부(churn_yn)별 평균 지표 ===')
compare_cols = ['recontact_rate', 'unresolved_rate', 'avg_csat', 'avg_nps', 'negative_voc_rate', 'data_gb_change_pct']
print(profile.groupby('churn_yn')[compare_cols].mean().round(2))
print()

print('=== 이탈 여부(churn_yn)별 각 지표의 유효 표본 수 (결측 제외) ===')
print(profile.groupby('churn_yn')[compare_cols].count())
print()

# 요금제 x 이탈 여부: 요금제를 통제했을 때도 같은 패턴이 나오는지 확인
print('=== 요금제 x 이탈 여부별 평균 지표 (요금제 통제) ===')
print(profile.groupby(['plan', 'churn_yn'])[compare_cols].mean().round(2))
print()

print('=== 요금제 x 이탈 여부별 표본 수 ===')
print(profile.groupby(['plan', 'churn_yn']).size().unstack('churn_yn'))
