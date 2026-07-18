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

satisfaction['csat'] = pd.to_numeric(satisfaction['csat'], errors='coerce')
consultations['is_recontact'] = consultations['is_recontact'].astype(str).str.strip().str.upper()

# consult_id 기준으로 직접 연결
joined = satisfaction.merge(
    consultations[['consult_id', 'channel', 'is_recontact']],
    on='consult_id',
    how='left',
)
joined = joined.dropna(subset=['channel'])

# 채널별 CSAT 평균과 재문의율 계산
channel_summary = (
    joined.groupby('channel')
    .agg(csat_mean=('csat', 'mean'), count=('csat', 'size'))
    .reset_index()
)

recontact_rate = (
    joined.groupby('channel')['is_recontact']
    .apply(lambda s: (s == 'Y').mean() * 100)
    .reset_index(name='recontact_rate')
)

summary = channel_summary.merge(recontact_rate, on='channel', how='left')
summary = summary.sort_values(['csat_mean', 'count'], ascending=[True, False])

# 시각화
fig, ax1 = plt.subplots(figsize=(9, 6))

# 막대: CSAT
bars = ax1.bar(
    summary['channel'],
    summary['csat_mean'],
    color='#1f77b4',
    width=0.6,
    alpha=0.9,
    label='CSAT 평균',
)
ax1.set_ylabel('CSAT 평균 (0~5)', color='#1f77b4')
ax1.set_ylim(0, 5)
ax1.tick_params(axis='y', labelcolor='#1f77b4')

# 꺾은선: 재문의율
ax2 = ax1.twinx()
ax2.plot(
    summary['channel'],
    summary['recontact_rate'],
    color='#d62728',
    marker='o',
    linewidth=2.5,
    markersize=8,
    label='재문의율',
)
ax2.set_ylabel('재문의율 (%)', color='#d62728')
ax2.set_ylim(0, 40)
ax2.tick_params(axis='y', labelcolor='#d62728')

# 제목/격자
ax1.set_title('채널별 CSAT 평균과 재문의율', fontsize=14, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.3)

# 범례 합치기
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

# 값 표시
for bar, value in zip(bars, summary['csat_mean']):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        f'{value:.2f}',
        ha='center',
        va='bottom',
        fontsize=9,
        color='#1f77b4',
    )

for x, value in enumerate(summary['recontact_rate']):
    ax2.text(
        x,
        value + 1.0,
        f'{value:.1f}%',
        ha='center',
        va='bottom',
        fontsize=9,
        color='#d62728',
    )

plt.tight_layout()

output_dir = base_dir / 'components' / 'output'
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / '04_채널별_CSAT_재문의.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f'저장 완료: {output_path}')
plt.show()
