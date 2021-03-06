from deployment.read_from_s3 import download_object_from_s3, download_csv_object_from_s3
from deployment.write_to_s3 import upload_output_to_s3
from src.constants.constants import *

from src.data.event_data.fetch_kw_format_dup_from_json import get_events_from_json
from src.data.fetch_kw_from_csv import get_events_from_csv
from src.data.trend_data.fetch_trend_data_with_date import fetch_trend_data_for_keywords
from src.features.event_vector_dup_kw import create_event_vector

from stock_analysis.iam_util.merge_cp_ip import create_combined_effective_points
from stock_analysis.moving_avg import model_impacts_for_stock_data
from stock_analysis.prophet_model import extract_changepoints_from_prophet

company = COMPANY_NAME
stock_data = STOCK_CSV
input_json = JFILE


def generate_impact_main(company_name, stock_csv_file, jfile):
    try:
        global event_list
        try:
            extract_changepoints_from_prophet(company_name, stock_csv_file)
        except BaseException as e:
            print("Error while extracting changepoints from prophet", e)
            return e

        try:
            model_impacts_for_stock_data(company_name, stock_csv_file)
        except BaseException as e:
            print("Error while modeling impacts", e)
            return e

        try:
            create_combined_effective_points(company_name)
        except BaseException as e:
            print("Error while creating effective points", e)
            return e

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
        #     return e

        try:
            fetch_trend_data_for_keywords(event_list, company_name, stock_csv_file)
        except BaseException as e:
            print("Error while fetching trends from keywords", e)
            return e

        try:
            create_event_vector(company_name)
        except BaseException as e:
            print("Error while creating event vector", e)
            return e

        try:
            upload_output_to_s3(OUTPUT_BUCKET, OUTPUT_IMPACTS_JSON_NAME, DESTINATION_OF_FINAL_OUTPUT_JSON)
        except BaseException as e:
            print("Error while uploading json to S3", e)
            return e

    except BaseException as error:
        return error


def trigger_main_process():
    try:
        download_object_from_s3(INPUT_BUCKET, INPUT_EVENTS_JSON_NAME, DESTINATION_TO_SAVE_INPUT_JSON)
        download_csv_object_from_s3(STOCK_DATA_BUCKET, STOCK_DATA_OBJECT_NAME, DESTINATION_TO_SAVE_CSV)
        # preprocess_stock_data(STOCK_CSV)
    except BaseException as e:
        print("Error while downloading from S3", e)
        return e

    generate_impact_main(company, stock_data, input_json)
