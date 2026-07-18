import pandas as pd
from pathlib import Path

sat = pd.read_csv(Path('raw') / 'data_satisfaction.csv')
cons = pd.read_csv(Path('raw') / 'data_consultations.csv')

# CSAT by channel using satisfaction records joined to consultations by consult_id
merged = sat.merge(cons[['consult_id', 'channel']], on='consult_id', how='left')
csat_stats = (
    merged.groupby('channel', dropna=False)
          .agg(csat_mean=('csat', 'mean'), satisfaction_count=('consult_id', 'count'))
          .reset_index()
)

# Recontact rate by channel from consultations data
recontact_stats = (
    cons.groupby('channel', dropna=False)
        .agg(recontact_rate=('is_recontact', lambda s: (s == 'Y').mean()), consult_count=('consult_id', 'count'))
        .reset_index()
)

combined = csat_stats.merge(recontact_stats, on='channel', how='left')
combined['csat_mean'] = combined['csat_mean'].round(2)
combined['recontact_rate'] = (combined['recontact_rate'] * 100).round(2)

# Compare direction: rank order and correlation
channels = combined['channel']
csat_rank = combined['csat_mean'].rank(method='min')
recontact_rank = combined['recontact_rate'].rank(method='min')
# Pearson correlation on the two metric vectors
corr = combined['csat_mean'].corr(combined['recontact_rate'])

print(combined.to_string(index=False))
print('correlation=', round(corr, 3))
print('rank_direction_match=', bool((csat_rank - recontact_rank).abs().sum() == 0))
