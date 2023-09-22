from flask import Flask, request, jsonify
from monitoring.prometheus import start_http_server,REQUEST_TIME,COUNT_p
import os
from prediction_validation_insertion import pred_validation
from predictFromModel import prediction
import time

app = Flask(__name__)

# Define Prometheus metrics

@REQUEST_TIME.time()
@app.route('/predict', methods=['POST'])
def predict():
  
    
    os.makedirs("raw_data", exist_ok=True)
    uploaded_file = request.files['file']
    
    if uploaded_file:
        file_path = os.path.join("raw_data", uploaded_file.filename)
        uploaded_file.save(file_path)
        
        path = "raw_data"
        pred_valid = pred_validation(path)
        pred_valid.prediction_validation()
        
        pred = prediction()
        result = pred.predictionfrommodel()
        
        COUNT_p.inc()
        return jsonify({'prediction': result.tolist()})
    
#@REQUEST_TIME.time()
@app.route('/get_prediction', methods=['GET'])
def get_prediction():
  
    start_time = time.time()
    file_path = "default_file"
    if file_path is not None:
        pred_valid = pred_validation(file_path)
        pred_valid.prediction_validation()
        
        pred = prediction()
        
        result = pred.predictionfrommodel()
        COUNT_p.inc()
        end_time= time.time()
        total_duration = end_time - start_time
        REQUEST_TIME.observe(total_duration)
        
        return jsonify({'prediction': result})

if __name__ == "__main__":
    # Start Prometheus HTTP server on port 8000 to scrape metrics
    start_http_server(8000)
    app.run(host='0.0.0.0', port=5000)
