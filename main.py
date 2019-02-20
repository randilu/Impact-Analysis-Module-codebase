from deployment.read_from_s3 import download_object_from_s3
from deployment.write_to_s3 import upload_output_to_s3

from src.data.event_data.fetch_kw_format_dup_from_json import get_events_from_json
from src.data.fetch_kw_from_csv import get_events_from_csv
from src.data.trend_data.fetch_trend_data_with_date import fetch_trend_data_for_keywords
from src.features.event_vector_dup_kw import create_event_vector

from stock_analysis.iam_util.merge_cp_ip import create_combined_effective_points
from stock_analysis.moving_avg import model_impacts_for_stock_data
from stock_analysis.prophet_model import extract_changepoints_from_prophet

company_name = 'kelani_valley'
jfile = "/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/events/eem/KelaniValleyPlantations2.json"
stock_csv_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/stock-data-companies/' + company_name + '.csv'
#
# manual input
#
events_csv_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/events/csv_files/events_of_kv_plus_plantations.csv'

input_s3_bucket_name = 'fypiamawsbucket'
input_object_name = 'KelaniValleyPlantations.json'
destination_to_save_input_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/events/eem/' + input_object_name

output_s3_bucket_name = 'fypiamawsbucket'
output_object_name = 'kelani_valley_impact_events.json'
source_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/final_output/' + output_object_name


def main():
    global event_list
    try:
        download_object_from_s3(input_s3_bucket_name, input_object_name, destination_to_save_input_file)
    except BaseException as e:
        print("Error while downloading from S3", e)

    try:
        extract_changepoints_from_prophet(company_name, stock_csv_file)
    except BaseException as e:
        print("Error while extracting changepoints from prophet", e)

    try:
        model_impacts_for_stock_data(company_name, stock_csv_file)
    except BaseException as e:
        print("Error while modeling impacts", e)

    try:
        create_combined_effective_points(company_name)
    except BaseException as e:
        print("Error while creating effective points", e)

    try:
        event_list = get_events_from_json(company_name, jfile)
    except BaseException as e:
        print("Error while fetching events from json", e)

    # #
    # # manual input
    # #
    #
    # try:
    #     event_list = get_events_from_csv(company_name, events_csv_file)
    # except BaseException as e:
    #     print("Error while fetching events from csv", e)

    try:
        fetch_trend_data_for_keywords(event_list, company_name, stock_csv_file)
    except BaseException as e:
        print("Error while fetching trends from keywords", e)

    try:
        create_event_vector(company_name)
    except BaseException as e:
        print("Error while creating event vector", e)

    try:
        upload_output_to_s3(output_s3_bucket_name, output_object_name, source_file)
    except BaseException as e:
        print("Error while uploading json to S3", e)


if __name__ == '__main__':
    main()
