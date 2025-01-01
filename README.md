# Weather App Backend Service

This project is a Flask-based backend service that interacts with the Open-Meteo Historical Weather API to fetch weather data for specific locations and date ranges, store the data in Google Cloud Storage (GCS), and provide endpoints to list and retrieve the stored files. The service is deployed on Google Cloud Run using Docker.

---

## Features

- Fetch historical weather data using the Open-Meteo API.
- Store fetched data as JSON files in Google Cloud Storage.
- List stored files in the GCS bucket.
- Retrieve and display the content of specific JSON files stored in GCS.

---

## Prerequisites

Before starting, ensure you have:

1. **Google Cloud Platform (GCP) Setup**:
   - A GCP project with billing enabled.
   - A Google Cloud Storage bucket created.
   - A service account with the `Storage Admin` role, and its JSON key downloaded.

2. **Installed Tools**:
   - [Python (3.8+)](https://www.python.org/downloads/)
   - [Docker](https://www.docker.com/products/docker-desktop)
   - [Google Cloud CLI (gcloud)](https://cloud.google.com/sdk/docs/install)

---

## Deployment Steps

### Step 1: Set Up Google Cloud

#### a. Create a Google Cloud Project
1. Log in to your Google Cloud Console: [https://console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project:
   - Go to **Manage Resources** > **Create Project**.
   - Name your project (e.g., `weather-app`) and note the **Project ID**.

#### b. Enable Necessary APIs
Run the following commands to enable the required APIs:
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable storage.googleapis.com
