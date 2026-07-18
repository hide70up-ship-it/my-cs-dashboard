import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 읽기
base_dir = Path(__file__).resolve().parents[1]
raw_dir = base_dir / 'raw'

customers = pd.read_csv(raw_dir / 'data_customers.csv')

# 요금제별 이탈율 계산 (요금제 등급 순서 고정: 베이직 -> 스탠다드 -> 프리미엄)
plan_order = ['베이직', '스탠다드', '프리미엄']
summary = (
    customers.groupby('plan')['churn_yn']
    .apply(lambda s: (s == 'Y').mean() * 100)
    .reindex(plan_order)
    .reset_index(name='churn_rate')
)

HIGHLIGHT_PLAN = '베이직'
HIGHLIGHT_COLOR = '#d03b3b'
MUTED_COLOR = '#b0aea6'
colors = [HIGHLIGHT_COLOR if plan == HIGHLIGHT_PLAN else MUTED_COLOR for plan in summary['plan']]

# 시각화
fig, ax = plt.subplots(figsize=(7, 6))

bars = ax.bar(
    summary['plan'],
    summary['churn_rate'],
    color=colors,
    width=0.5,
)

ax.set_ylabel('이탈율 (%)')
ax.set_ylim(0, summary['churn_rate'].max() * 1.25)
ax.set_title('요금제별 이탈율', fontsize=14, fontweight='bold')
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 값 표시 (막대 끝, 텍스트는 데이터 색이 아닌 잉크 색 사용)
for bar, value in zip(bars, summary['churn_rate']):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + summary['churn_rate'].max() * 0.02,
        f'{value:.2f}%',
        ha='center',
        va='bottom',
        fontsize=11,
        fontweight='bold',
        color='#0b0b0b',
    )

plt.tight_layout()

output_dir = base_dir / 'components' / 'output'
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / '05_요금제별_이탈율.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f'저장 완료: {output_path}')
plt.show()
