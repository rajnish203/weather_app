import os
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
from google.cloud import storage
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Google Cloud Storage Configuration
GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")
GCP_SERVICE_ACCOUNT_KEY = os.getenv("GCP_SERVICE_ACCOUNT_KEY")

# Initialize the Google Cloud Storage client using the service account key
GCS_CLIENT = storage.Client.from_service_account_json(GCP_SERVICE_ACCOUNT_KEY)

# Open-Meteo API Endpoint
OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"


@app.route('/')
def home():
    """
    Home route to render the main page with input form.
    """
    return render_template('index.html')


@app.route('/store-weather-data', methods=['POST'])
def store_weather_data():
    """
    Fetches weather data for a specific location and date range from the Open-Meteo API
    and stores it in Google Cloud Storage.
    """
    try:
        data = request.form
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not latitude or not longitude or not start_date or not end_date:
            return jsonify({"error": "Missing required parameters"}), 400

        # Fetch weather data from Open-Meteo API
        response = requests.get(OPEN_METEO_URL, params={
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "temperature_2m_mean",
                "apparent_temperature_max",
                "apparent_temperature_min",
                "apparent_temperature_mean"
            ],
            "timezone": "auto"
        })

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch weather data from Open-Meteo API"}), 500

        weather_data = response.json()

        # Save data to Google Cloud Storage
        file_name = f"weather_{latitude}_{longitude}_{start_date}_to_{end_date}.json"
        bucket = GCS_CLIENT.bucket(GCP_BUCKET_NAME)
        blob = bucket.blob(file_name)
        blob.upload_from_string(json.dumps(weather_data), content_type='application/json')

        return redirect(url_for('list_weather_files'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/list-weather-files', methods=['GET'])
def list_weather_files():
    """
    Lists all JSON weather data files stored in the Google Cloud Storage bucket.
    """
    try:
        bucket = GCS_CLIENT.bucket(GCP_BUCKET_NAME)
        blobs = bucket.list_blobs()
        files = [blob.name for blob in blobs]
        return render_template('weather_files.html', files=files)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/weather-file-content/<file_name>', methods=['GET'])
def weather_file_content(file_name):
    """
    Fetches and displays the content of a specific JSON file stored in Google Cloud Storage.
    """
    try:
        bucket = GCS_CLIENT.bucket(GCP_BUCKET_NAME)
        blob = bucket.blob(file_name)

        if not blob.exists():
            return jsonify({"error": "File not found"}), 404

        file_content = blob.download_as_text()
        json_content = json.loads(file_content)  # Parse JSON for better representation
        return render_template('file_content.html', file_name=file_name, content=json.dumps(json_content, indent=4))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Run the Flask app locally
    app.run(host="0.0.0.0", port=8080)
