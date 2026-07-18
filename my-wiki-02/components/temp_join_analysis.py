import pandas as pd
from pathlib import Path

sat = pd.read_csv(Path('raw') / 'data_satisfaction.csv')
cons = pd.read_csv(Path('raw') / 'data_consultations.csv')
cust = pd.read_csv(Path('raw') / 'data_customers.csv')

merged = (
    sat.merge(cons[['consult_id', 'category', 'channel']], on='consult_id', how='left')
       .merge(cust[['customer_id', 'plan', 'region']], on='customer_id', how='left')
)

print(merged[['consult_id', 'category', 'channel', 'plan', 'region', 'csat', 'nps']].head().to_string(index=False))
print('shape', merged.shape)
