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

# consult_id 기준으로 직접 연결
joined = satisfaction.merge(
    consultations[['consult_id', 'category']],
    on='consult_id',
    how='left',
)

# category별 CSAT 평균 및 건수
summary = (
    joined.groupby('category', dropna=False)
    .agg(csat_mean=('csat', 'mean'), count=('csat', 'size'))
    .reset_index()
)
summary = summary.sort_values(['csat_mean', 'count'], ascending=[True, False])

# 전체 평균 기준선
overall_mean = summary['csat_mean'].mean()

# 시각화
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#d62728' if i < 2 else '#bdbdbd' for i in range(len(summary))]

bars = ax.bar(summary['category'], summary['csat_mean'], color=colors, edgecolor='#666666', linewidth=0.8)

# 기준선 추가
ax.axhline(overall_mean, color='#2f4f4f', linestyle='--', linewidth=1.5, label=f'전체 평균 {overall_mean:.2f}')

# 막대 위 건수 표시
for bar, count in zip(bars, summary['count']):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.02,
        f'n={count}',
        ha='center',
        va='bottom',
        fontsize=8,
        color='#555555',
    )

# 축 설정
ax.set_title('상담 category별 CSAT 평균', fontsize=14, fontweight='bold')
ax.set_ylabel('CSAT 평균 (5점 만점)')
ax.set_xlabel('상담 category')
ax.set_ylim(0, max(4.2, summary['csat_mean'].max() + 0.3))
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

# x축 라벨 회전
plt.setp(ax.get_xticklabels(), rotation=0, ha='center')

# 범례
ax.legend(loc='upper right')

# 출력 경로
output_dir = base_dir / 'components' / 'output'
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / '03_카테고리별_저만족도.png'
plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f'저장 완료: {output_path}')
plt.show()
