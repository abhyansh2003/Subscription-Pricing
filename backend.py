from flask import Flask, request, jsonify
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB limit

BASE_PRICE = 100
PRICE_PER_CREDIT_LINE = 10
PRICE_PER_CREDIT_SCORE_POINT = 0.5

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def load_and_process_csv(csv_file_path):
    df = pd.read_csv('user_data.csv')
    df.columns = df.columns.str.strip().str.lower()
    expected_columns = ['creditscore', 'creditlines', 'subscriptionprice']
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        return None, missing_columns
    else:
        df = df[expected_columns]
        return df, None

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        df = pd.read_csv(filepath)
        if 'CreditScore' not in df.columns or 'CreditLines' not in df.columns:
            return jsonify({'error': 'Invalid CSV format'}), 400

        df['SubscriptionPrice'] = BASE_PRICE + (PRICE_PER_CREDIT_LINE * df['CreditLines']) + (PRICE_PER_CREDIT_SCORE_POINT * df['CreditScore'])
        df.to_csv(filepath, index=False)  # Save the processed file

        return jsonify({'filename': filename}), 200
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/data/<filename>', methods=['GET'])
def get_data(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    df = pd.read_csv(filepath)
    return df.to_json(orient='records'), 200

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='127.0.0.1', port=5000)
