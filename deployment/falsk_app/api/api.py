import flask
from flask import request, Response

from deployment.falsk_app.api_handler import generate_results_api_handler
from src.features.event_vector_dup_kw import create_event_vector

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


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=res,
        status=status_code
    )


app.run()
