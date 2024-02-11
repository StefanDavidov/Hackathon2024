from flask import Flask, request, jsonify

import sys
sys.path.append('../../model')
from testModel import forecast_test_data

app = Flask(__name__)

@app.route('/api/getPrediction', methods=['POST'])
def get_prediction():
    data = request.get_json()
    # Process the data here using your Python script
    result = forecast_test_data(data["company"])
    return jsonify({'output': result})

if __name__ == '__main__':
    app.run(debug=True)