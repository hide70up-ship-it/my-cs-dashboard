import pandas as pd
from pathlib import Path

sat = pd.read_csv(Path('raw') / 'data_satisfaction.csv')
cons = pd.read_csv(Path('raw') / 'data_consultations.csv')
cust = pd.read_csv(Path('raw') / 'data_customers.csv')

merged = (
    sat.merge(cons[['consult_id', 'category', 'channel']], on='consult_id', how='left')
       .merge(cust[['customer_id', 'plan', 'region']], on='customer_id', how='left')
)

# 1. category
cat_stats = (
    merged.groupby('category', dropna=False)
          .agg(csat_mean=('csat', 'mean'), nps_mean=('nps', 'mean'), count=('consult_id', 'count'))
          .reset_index()
          .sort_values(['csat_mean', 'count'], ascending=[True, False])
)
cat_stats['sample_flag'] = cat_stats['count'] < 30
cat_stats['csat_mean'] = cat_stats['csat_mean'].round(2)
cat_stats['nps_mean'] = cat_stats['nps_mean'].round(2)

# 2. channel
ch_stats = (
    merged.groupby('channel', dropna=False)
          .agg(csat_mean=('csat', 'mean'), nps_mean=('nps', 'mean'), count=('consult_id', 'count'))
          .reset_index()
          .sort_values(['csat_mean', 'count'], ascending=[True, False])
)
ch_stats['sample_flag'] = ch_stats['count'] < 30
ch_stats['csat_mean'] = ch_stats['csat_mean'].round(2)
ch_stats['nps_mean'] = ch_stats['nps_mean'].round(2)

# 3. plan
plan_stats = (
    merged.groupby('plan', dropna=False)
          .agg(csat_mean=('csat', 'mean'), count=('consult_id', 'count'))
          .reset_index()
          .sort_values(['csat_mean', 'count'], ascending=[True, False])
)
plan_stats['sample_flag'] = plan_stats['count'] < 30
plan_stats['csat_mean'] = plan_stats['csat_mean'].round(2)

# 4. region
region_stats = (
    merged.groupby('region', dropna=False)
          .agg(csat_mean=('csat', 'mean'), count=('consult_id', 'count'))
          .reset_index()
          .sort_values(['csat_mean', 'count'], ascending=[True, False])
)
region_stats['sample_flag'] = region_stats['count'] < 30
region_stats['csat_mean'] = region_stats['csat_mean'].round(2)

print('=== CATEGORY ===')
print(cat_stats.to_string(index=False))
print('\n=== CHANNEL ===')
print(ch_stats.to_string(index=False))
print('\n=== PLAN ===')
print(plan_stats.to_string(index=False))
print('\n=== REGION ===')
print(region_stats.to_string(index=False))
