import pandas as pd

from src.data.fetch_trend_data_utils import display_max_cols, create_json_from_df, write_json_data_to_file

# company_name = 'kelani_valley'
# display_max_cols(100)


def create_event_vector(company_name):
    try:
        impact_df = pd.read_csv(
            '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/events_impacted/' + company_name + '_events_mapped.csv'
            , sep='\t', encoding='utf-8')
        # print(impact_df)

        event_df = impact_df[['date', 'kw_max', 'max_value', 'close', 'impact', 'daily_news_vector_sum']]
        event_df['kw_max'], event_df['event_no'] = event_df['kw_max'].str.split('_', 1).str
        event_df['event_no'].dropna(inplace=True)
        event_df['event_no'] = event_df['event_no'].astype(int)

        # print(event_df)

        event_dictionary_df = pd.read_csv(
            '/home/randilu/fyp_integration/Impact-Analysis-Module/src/data/dictionaries/' + company_name + '_event_dictionary.csv',
            sep=',', encoding='utf-8')

        # print(event_dictionary_df)
        combined_event_impact_df = pd.merge(event_df, event_dictionary_df, on=['event_no'], how='left')
        combined_event_impact_df.dropna(inplace=True)
        columns = ['event_no', 'keyword_1']
        combined_event_impact_df.drop(columns, inplace=True, axis=1)

        print(combined_event_impact_df)
        combined_event_impact_df.to_csv(
            '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/final_output/' + company_name + '_impact_events.csv')
        events_impact_json = create_json_from_df(combined_event_impact_df)
        print(events_impact_json)
        write_json_data_to_file(
            '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/final_output/' + company_name + '_impact_events.json',
            events_impact_json)
        return events_impact_json

    except BaseException as e:
        return e

    # try:
#     session = boto3.Session(
#         aws_access_key_id='AKIAJC7S24JKRFDQAGVA',
#         aws_secret_access_key='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',
#     )
#     s3 = session.resource('s3')
#     s3.Object('finalyearprojectresources', 'impacts.json').put(Body=events_impact_json)
#     print('Uploaded')
#
# except BaseException as e:
#     print('Upload error')
#     print(str(e))

# #
# # run manually
# #
#
# create_event_vector(company_name)
