import flask
from flask import request
from deployment.falsk_app.api_handler import generate_results_api_handler
from deployment.falsk_app.api_utils import custom_response, start_runner
from deployment.notifications import alert_for_sqs_notifications
from src.features.event_vector_dup_kw import create_event_vector

import requests
import threading
import time

app = flask.Flask(__name__)
# to get more specialized error messages
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Impact Analysis Module</h1><p>Find the impact of news events on stock prices using Google trends.</p>"


@app.route('/iam/api/v1/resources/events/impacts/<company_name>', methods=['GET'])
def get_result_impacts(company_name):
    impacts = create_event_vector(company_name)
    return custom_response(impacts, 200)


@app.route('/iam/api/v1/resources/events', methods=['POST'])
def generate_results():
    if request.content_type != "application/json":
        error = {'error': 'Invalid Content Type'}
        return custom_response(error, 400)

    req_data = request.get_json()
    print(req_data)
    resp, error = generate_results_api_handler(req_data)

    if error:
        return custom_response(error, 500)

    return custom_response(resp, 201)


# @app.before_first_request
def activate_job():
    def run_job():
        print("Searching for SQS notifications...")
        alert_for_sqs_notifications()
            # time.sleep(2)
    run_job()

    thread = threading.Thread(target=activate_job())
    thread.start()


if __name__ == "__main__":
    # activate_job()
    # start_runner()
    app.run()
    # activate_job()

