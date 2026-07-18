import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# raw/data_voc.csv에서 해지관련 + 부정 VOC 원문을 다시 읽어 집계
voc = pd.read_csv(Path(__file__).resolve().parents[1] / 'raw' / 'data_voc.csv')
subset = voc[(voc['category'] == '해지관련') & (voc['sentiment'] == '부정')]['content']
counts = subset.value_counts().reset_index()
counts.columns = ['content', 'count']

# 긴 라벨을 적당히 줄바꿈
label_map = {
    '해지하려는데 위약금 설명이 너무 복잡해요. 명확하게 알려주세요.': '해지하려는데 위약금 설명이\n너무 복잡해요. 명확하게 알려주세요.',
    '해지 신청 후에도 요금이 계속 청구되고 있어요.': '해지 신청 후에도 요금이\n계속 청구되고 있어요.',
    '번호이동 신청했는데 일주일이 지나도 진행이 안 되고 있어요.': '번호이동 신청했는데\n일주일이 지나도 진행이 안 되고 있어요.'
}
counts['label'] = counts['content'].map(label_map)

# 건수가 많은 유형이 위로 오게 정렬
counts = counts.sort_values('count', ascending=False).reset_index(drop=True)

plt.rcParams['font.family'] = 'Malgun Gothic'
fig, ax = plt.subplots(figsize=(10, 4))

bars = ax.barh(counts['label'], counts['count'], color='#4C78A8')
ax.invert_yaxis()

# 막대 끝에 건수 숫자 표시
for bar, value in zip(bars, counts['count']):
    ax.text(value + 0.6, bar.get_y() + bar.get_height() / 2, str(value), va='center', ha='left', fontsize=11)

ax.set_title('해지관련 부정 VOC 유형별 건수', fontsize=14)
ax.set_xlabel('건수')
ax.set_ylabel('유형')
ax.set_xlim(0, max(counts['count']) + 8)
ax.grid(axis='x', linestyle='--', alpha=0.3)

plt.tight_layout()
output_path = Path(__file__).resolve().parent / '02_해지관련_불만유형.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f'저장 완료: {output_path}')
plt.show()
