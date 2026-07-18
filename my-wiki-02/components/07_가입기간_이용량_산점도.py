import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

base_dir = Path(__file__).resolve().parents[1]
raw_dir = base_dir / 'raw'

customers = pd.read_csv(raw_dir / 'data_customers.csv')
profile = pd.read_csv(base_dir / 'components' / 'output' / '06_customers_full_profile.csv')

# 가입기간(개월수): 가입일 ~ 2024-12-31 기준, 구간화하지 않고 연속값 그대로 사용
customers['join_date'] = pd.to_datetime(customers['join_date'])
ref_date = pd.Timestamp('2024-12-31')
customers['tenure_months'] = (ref_date - customers['join_date']).dt.days / 30.44

data = customers[['customer_id', 'plan', 'tenure_months']].merge(
    profile[['customer_id', 'avg_data_gb']], on='customer_id', how='left'
).dropna(subset=['avg_data_gb'])

overall_corr = data['tenure_months'].corr(data['avg_data_gb'])

# 요금제는 이용량 총량(베이직<스탠다드<프리미엄)을 그대로 반영하는 순서형 변수이므로
# 한 계열(blue) 안에서 밝기 단계만 다르게 준다 (색상군을 새로 배정하지 않음).
plan_order = ['베이직', '스탠다드', '프리미엄']
plan_colors = {'베이직': '#6da7ec', '스탠다드': '#2a78d6', '프리미엄': '#184f95'}

fig, ax = plt.subplots(figsize=(8, 6))

corr_lines = []
for plan in plan_order:
    sub = data[data['plan'] == plan]
    x, y = sub['tenure_months'], sub['avg_data_gb']
    r = x.corr(y)
    corr_lines.append(f'{plan}: r = {r:.3f} (n={len(sub)})')

    ax.scatter(x, y, s=26, color=plan_colors[plan], alpha=0.55, edgecolors='none', label=plan)

    slope, intercept = np.polyfit(x, y, 1)
    x_line = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_line, slope * x_line + intercept, color=plan_colors[plan], linewidth=2, linestyle='--')

ax.set_xlabel('가입기간 (개월)')
ax.set_ylabel('월평균 이용량 (GB)')
ax.set_title('가입기간과 월평균 이용량의 관계 (요금제 통제)', fontsize=14, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(loc='upper right', frameon=False, title='요금제')

info_text = f'전체 r = {overall_corr:.3f} (요금제 미통제)\n' + '\n'.join(corr_lines)
ax.text(
    0.02, 0.98, info_text,
    transform=ax.transAxes, ha='left', va='top', fontsize=10, color='#0b0b0b',
)

plt.tight_layout()

output_dir = base_dir / 'components' / 'output'
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / '07_가입기간_이용량_산점도.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f'저장 완료: {output_path}')
print(f'전체 r (요금제 미통제): {overall_corr:.4f}')
for line in corr_lines:
    print(line)
