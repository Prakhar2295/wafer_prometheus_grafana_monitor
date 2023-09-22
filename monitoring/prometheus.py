from prometheus_client import Summary,Counter,start_http_server


REQUEST_TIME = Summary('request_processing_seconds','Time Spent processing request')
COUNT_p = Counter("total_prediction_hits","Invoke Message")

