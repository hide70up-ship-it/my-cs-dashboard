import pandas as pd
from pathlib import Path

voc = pd.read_csv(Path('raw') / 'data_voc.csv')
voc['received_date'] = pd.to_datetime(voc['received_date'], errors='coerce')

# 1. voc_type
voc_type = voc['voc_type'].value_counts(dropna=False).rename_axis('voc_type').reset_index(name='count')
voc_type['ratio_pct'] = voc_type['count'] / len(voc) * 100

# 2. category
category = voc.groupby('category', dropna=False).agg(
    total_count=('voc_id', 'count'),
    negative_count=('sentiment', lambda s: (s == '부정').sum()),
).reset_index()
category['negative_ratio_pct'] = category['negative_count'] / category['total_count'] * 100

# 3. monthly
monthly = voc.set_index('received_date').resample('ME').agg(
    total_count=('voc_id', 'count'),
    negative_count=('sentiment', lambda s: (s == '부정').sum()),
).reset_index()
monthly['month'] = monthly['received_date'].dt.strftime('%Y-%m')
monthly = monthly[['month', 'total_count', 'negative_count']]

print('=== VOC_TYPE ===')
print(voc_type.to_string(index=False))
print('\n=== CATEGORY ===')
print(category.to_string(index=False))
print('\n=== MONTHLY ===')
print(monthly.to_string(index=False))
