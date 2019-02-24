COMPANY_NAME = 'kelani_valley'
BASE_PATH = '/home/randilu/fyp_integration/Impact-Analysis-Module'

# TODO genaralize jfile
JFILE = BASE_PATH + '/data/external/events/eem/data.json'
STOCK_CSV = BASE_PATH + '/data/external/stock-data-companies/' + COMPANY_NAME + '.csv'
#
# manual input
#
# TODO
INPUT_EVENTS_CSV = BASE_PATH + '/data/external/events/csv_files/events_of_kv_plus_plantations.csv'
IMPACT_EVENTS_CSV = BASE_PATH + '/data/processed/final_output/' + COMPANY_NAME + '_impact_events.csv'

INPUT_BUCKET = 'fypiamawsbucket'
INPUT_EVENTS_JSON_NAME = 'KelaniValleyPlantations.json'
DESTINATION_TO_SAVE_INPUT_JSON = BASE_PATH + '/data/external/events/eem/' + INPUT_EVENTS_JSON_NAME

OUTPUT_BUCKET = 'fypiamawsbucket'
OUTPUT_IMPACTS_JSON_NAME = 'kelani_valley_impact_events.json'
DESTINATION_OF_FINAL_OUTPUT_JSON = BASE_PATH + '/data/processed/final_output/' + OUTPUT_IMPACTS_JSON_NAME

# stock data
input_stock_file_name = 'company_history.csv'
destination_to_save_input_stock_file = BASE_PATH + '/data/external/stock-data-companies/' + input_stock_file_name + '.csv'

#
# AWS details
#
USER1_ACCESS_ID = 'AKIAIR6DQWSOVXCJAXPA'
USER1_ACCESS_KEY = 't5EMmjUapCKo/Ta2S1QUmCQWEsY3HOQwXCqL7+Hy'

SQS_QUEUE_NAME = 'fyp_company_dataq'

# company_name = 'kelani_valley'
# jfile = "/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/events/eem/data.json"
# stock_csv_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/stock-data-companies/' + company_name + '.csv'
# # #
# # manual input
# #
# events_csv_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/events/csv_files/events_of_kv_plus_plantations.csv'

# input_s3_bucket_name = 'fypiamawsbucket'
# input_object_name = 'KelaniValleyPlantations.json'
# destination_to_save_input_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/events/eem/' + input_object_name
#
# output_s3_bucket_name = 'fypiamawsbucket'
# output_object_name = 'kelani_valley_impact_events.json'
# source_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/final_output/' + output_object_name
