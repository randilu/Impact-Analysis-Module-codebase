import json

from deployment.falsk_app.process import generate_impact_main
from src.data.fetch_trend_data_utils import read_json_data_from_file

# jfile = "/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/events/eem/KelaniValleyPlantations2.json"
# json_data = read_json_data_from_file(jfile)


def generate_results_api_handler(json_data):
    input_object_name = 'KelaniValleyPlantations.json'
    destination_to_save_input_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/events/eem/' + input_object_name
    msg = None
    error = None
    try:
        with open(destination_to_save_input_file, 'w') as outfile:
            json.dump(json_data, outfile)

        #
        # Trigger main process
        #
        generate_impact_main()
        msg = {'File Successfully Processed!'}
        # return msg

    except IOError as e:
        error = {"Error handling the request", e}
        # return error

    return msg, error

# #
# # run manually
# #
# generate_results_api_handler(json_data)
