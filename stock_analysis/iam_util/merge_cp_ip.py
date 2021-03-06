import pandas as pd


def create_combined_effective_points(company_name):
    changepoints_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/stock_analysis/data/changepoints/' + company_name + '_changepoints.csv'
    impactpoints_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/stock_analysis/data/changepoints/' + company_name + '_impactpoints.csv'
    effective_points_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/changepoints/' + company_name + '_effective_points.csv'

    # reading from csv
    cp_df = pd.read_csv(changepoints_file, sep='\t', encoding='utf-8', index_col='date', parse_dates=True)
    ip_df = pd.read_csv(impactpoints_file, sep='\t', encoding='utf-8', index_col='date', parse_dates=True)

    print(cp_df)
    print(ip_df)
    # frames = [ip_df, cp_df]

    effective_dates = cp_df.append(ip_df)
    effective_dates.drop_duplicates(keep=False, inplace=True)
    effective_dates.dropna(inplace=True)
    effective_dates.reset_index(level=0, inplace=True)
    effective_dates['week_number'] = effective_dates['date'].dt.week
    effective_dates.drop_duplicates(subset='week_number', keep='first', inplace=True)
    effective_dates.drop(columns='week_number', inplace=True)
    effective_dates = effective_dates.set_index('date')
    effective_dates.sort_index(inplace=True, ascending=False)
    print(effective_dates)

    effective_dates.to_csv(effective_points_file, sep='\t', encoding='utf-8')
    effective_dates.to_csv()

