COMPANY_NAME = 'kelani_valley'
BASE_PATH = '/home/randilu/fyp_integration/Impact-Analysis-Module'

# genaralize jfile
JFILE = BASE_PATH + '/data/external/events/eem/company_events.json'
STOCK_CSV = BASE_PATH + '/data/external/stock-data-companies/' + COMPANY_NAME + '.csv'
#
# manual input
#
INPUT_EVENTS_CSV = BASE_PATH + '/data/external/events/csv_files/'+COMPANY_NAME+'_events.csv'
IMPACT_EVENTS_CSV = BASE_PATH + '/data/processed/final_output/' + COMPANY_NAME + '_impact_events.csv'

INPUT_BUCKET = 'fypiamawsbucket'
INPUT_EVENTS_JSON_NAME = 'company_events.json'
DESTINATION_TO_SAVE_INPUT_JSON = BASE_PATH + '/data/external/events/eem/' + INPUT_EVENTS_JSON_NAME

OUTPUT_BUCKET = 'pythonpackages-3.6'
OUTPUT_IMPACTS_JSON_NAME = 'impacts.json'
DESTINATION_OF_FINAL_OUTPUT_JSON = BASE_PATH + '/data/processed/final_output/' + OUTPUT_IMPACTS_JSON_NAME


#
# My AWS details
#
USER1_ACCESS_ID = ''
USER1_ACCESS_KEY = ''

SQS_QUEUE_NAME = 'fyp_company_dataq'

# perf iso
USER2_ACCESS_ID = ''
USER2_ACCESS_KEY = ''

# stock data
STOCK_DATA_BUCKET = 'finalyearprojectresources'
STOCK_DATA_OBJECT_NAME = 'company_stocks.csv'
DESTINATION_TO_SAVE_CSV = BASE_PATH + '/data/external/stock-data-companies/' + COMPANY_NAME + '.csv'
USER3_ACCESS_ID = ''
USER3_ACCESS_KEY = ''

