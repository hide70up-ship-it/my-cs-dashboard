import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 읽기
base_dir = Path(__file__).resolve().parents[1]
raw_dir = base_dir / 'raw'

satisfaction = pd.read_csv(raw_dir / 'data_satisfaction.csv')
consultations = pd.read_csv(raw_dir / 'data_consultations.csv')
customers = pd.read_csv(raw_dir / 'data_customers.csv')

# 데이터 연결: satisfaction -> consultations (consult_id 기준) -> customers (상담의 customer_id 기준)
consultations_for_join = consultations[['consult_id', 'customer_id', 'consult_date', 'channel', 'category', 'duration_min', 'status', 'is_recontact', 'agent_id']].rename(columns={'customer_id': 'consult_customer_id'})
customers_for_join = customers[['customer_id', 'region', 'plan', 'churn_yn']].rename(columns={'customer_id': 'customer_id_customer'})

joined = satisfaction.merge(
    consultations_for_join,
    on='consult_id',
    how='left',
)

joined = joined.merge(
    customers_for_join,
    left_on='consult_customer_id',
    right_on='customer_id_customer',
    how='left',
)

joined['customer_id'] = joined['consult_customer_id']
joined = joined.drop(columns=['consult_customer_id', 'customer_id_customer'])

# 연결 결과 확인
matched_count = joined['consult_date'].notna().sum()
unmatched_count = (joined['consult_date'].isna()).sum()
print(f'연결된 응답 수: {matched_count}')
print(f'미연결 응답 수: {unmatched_count}')

csat = joined['csat'].astype(float)
nps = joined['nps'].astype(float)

# 기본 지표 계산
csat_avg = csat.mean()
nps_avg = nps.mean()

# NPS 그룹 분류
nps_groups = pd.cut(
    nps,
    bins=[-1, 6, 8, 10],
    labels=['비판자', '중립자', '추천자'],
    include_lowest=True,
    right=True,
)

detractor_rate = (nps_groups == '비판자').mean() * 100
promoter_rate = (nps_groups == '추천자').mean() * 100
nps_score = promoter_rate - detractor_rate

# 저만족 비율
low_satisfaction_rate = ((csat >= 1) & (csat <= 2)).mean() * 100

# 카드 구성 정보
cards = [
    {
        'title': 'CSAT 평균',
        'value': f'{csat_avg:.2f}',
        'subtitle': '5점 만점 · 만족도 중심 지표',
        'color': '#1f77b4',
    },
    {
        'title': 'NPS 평균',
        'value': f'{nps_avg:.2f}',
        'subtitle': '10점 만점 · 참고용 평균',
        'color': '#6c757d',
    },
    {
        'title': 'NPS 점수',
        'value': f'{nps_score:.1f}',
        'subtitle': '추천자 비율 − 비판자 비율',
        'color': '#d62728' if nps_score < 0 else '#2ca02c',
    },
    {
        'title': '저만족 비율',
        'value': f'{low_satisfaction_rate:.1f}%',
        'subtitle': 'CSAT 1~2점 응답 비율',
        'color': '#ff7f0e',
    },
]

# 그리기
fig, axes = plt.subplots(1, 4, figsize=(16, 5), constrained_layout=True)
fig.patch.set_facecolor('#f7f7f7')

for ax, card in zip(axes, cards):
    ax.set_facecolor('white')
    ax.set_aspect('auto')

    # 제목
    ax.text(0.5, 0.78, card['title'], ha='center', va='center', fontsize=14, color='#333333')

    # 핵심 숫자
    ax.text(0.5, 0.52, card['value'], ha='center', va='center', fontsize=28, fontweight='bold', color=card['color'])

    # 설명
    ax.text(0.5, 0.25, card['subtitle'], ha='center', va='center', fontsize=11, color='#555555', wrap=True)

    # 카드 테두리
    for spine in ax.spines.values():
        spine.set_color('#d0d0d0')
        spine.set_linewidth(1.2)

    ax.set_xticks([])
    ax.set_yticks([])

# NPS 점수 카드에 작은 게이지 바 추가
nps_ax = axes[2]
value = nps_score
bar_value = max(min(value, 100), -100)
bar_width = 0.8
bar_height = 0.16

# 게이지 바 위치
x0 = 0.12
x1 = 0.88
bar_left = x0
bar_right = x0 + (bar_width * (bar_value / 100))

# 실제 값이 음수면 왼쪽에서부터 채우기
if value < 0:
    bar_left = x0 + (bar_width * ((-value) / 100))
    bar_right = x0 + bar_width

# 바 배경
nps_ax.add_patch(plt.Rectangle((0.12, 0.06), 0.76, 0.12, transform=nps_ax.transAxes, facecolor='#eeeeee', edgecolor='none'))
# 바 채움
nps_ax.add_patch(plt.Rectangle((bar_left, 0.06), max(0.0, bar_right - bar_left), 0.12, transform=nps_ax.transAxes, facecolor='#d62728' if value < 0 else '#2ca02c', edgecolor='none'))

# 눈금과 값 표시
nps_ax.text(0.12, 0.02, '-100', ha='left', va='top', fontsize=9, color='#666666')
nps_ax.text(0.88, 0.02, '+100', ha='right', va='top', fontsize=9, color='#666666')
nps_ax.text(0.5, 0.02, f'{value:.1f}', ha='center', va='top', fontsize=10, fontweight='bold', color='#222222')

# 전체 제목
fig.suptitle('만족도 현황 스코어카드', fontsize=18, fontweight='bold', y=0.98)

output_dir = Path(__file__).resolve().parent / 'output'
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / '02_csat_nps_scorecard.png'
joined_output_path = output_dir / '02_joined_satisfaction_consultations_customers.csv'

joined.to_csv(joined_output_path, index=False)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f'저장 완료: {output_path}')
print(f'연결 데이터 저장: {joined_output_path}')
plt.show()
