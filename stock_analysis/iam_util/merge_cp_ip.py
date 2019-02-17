import pandas as pd

changepoints_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/stock_analysis/data/changepoints/changepoints.csv'
impactpoints_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/stock_analysis/data/changepoints/impactpoints.csv'
effective_points_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/changepoints/effective_points.csv'

# reading from csv
cp_df = pd.read_csv(changepoints_file, sep='\t', encoding='utf-8', index_col='date', parse_dates=True)
ip_df = pd.read_csv(impactpoints_file, sep='\t', encoding='utf-8', index_col='date', parse_dates=True)

print(cp_df)
print(ip_df)
frames = [ip_df, cp_df]

effective_dates = cp_df.append(ip_df)
effective_dates.dropna(inplace=True)
effective_dates.sort_index(inplace=True, ascending=False)
print(effective_dates)

effective_dates.to_csv(effective_points_file, sep='\t', encoding='utf-8')
effective_dates.to_csv()
