from flask import request, Response
import requests
import threading
import time


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=res,
        status=status_code
    )


def start_runner():
    def start_loop():
        start_loop()
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('http://127.0.0.1:5000/')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)


# @app.before_first_request
# def activate_notifications():
#     def run_job():
#         # status = True
#         while True:
#             print("Searching for SQS notifications...")
#             # status = alert_for_sqs_notifications()
#             time.sleep(3)
#         # return
#
#     thread = threading.Thread(target=run_job)
#     thread.start()
#
#
# if __name__ == "__main__":
#     # trigger for request
#     # start_runner()
#     app.run()
#     activate_notifications()
