from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)
model = joblib.load('KNN5Feature.pkl')

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/predict', methods=['POST'])
def predict():
    error_message = None

    # Jika file diunggah
    if 'file' in request.files:
        file = request.files['file']
        if file:
            required_columns = ['pkts', 'bytes', 'spkts', 'sbytes', 'TnBPDstIP']

            df = pd.read_csv(file)
            df_selected = df[required_columns]
            prediction = model.predict(df_selected.values).tolist()  # Convert to list for JSON compatibility

            # Include each row's data and prediction
            data = [{'type': 'multiple', 
                     'prediction': prediction, 
                     'data': df_selected.to_dict(orient='records')}]  # Convert df to list of dictionaries
            return jsonify({'data': data})
            
    # Jika input manual
    if 'pkts' in request.form and 'bytes' in request.form and 'spkts' in request.form and 'sbytes' in request.form and 'TnBPDstIP' in request.form:
        pkts = float(request.form['pkts'])
        bytes = float(request.form['bytes'])
        spkts = float(request.form['spkts'])
        sbytes = float(request.form['sbytes'])
        TnBPDstIP = float(request.form['TnBPDstIP'])

        input_features = np.array([[pkts, bytes, spkts, sbytes, TnBPDstIP]])

        prediction = model.predict(input_features)
        data = [{'type': 'single', 'prediction': int(prediction[0])}]
        return jsonify({'data': data})

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)
