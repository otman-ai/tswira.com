# Reelze.app - Server-Side (Django) README

## Overview

Reelze.app is a platform that generates faceless shorts. This repository contains the server-side code built using Django. This README provides instructions on how to set up and run the server, as well as a breakdown of its main components.

## Requirements

To run the Django server, you'll need the following software:

- **Python 3.8+**: The backend is built with Python, so you'll need to install it from [here](https://www.python.org/downloads/).
- **Git**: For version control.
- **pip**: Python package manager to install the necessary dependencies.

AND also you will need to setup your STRIPE keys in .env, AWS keys for storing the videos, Google cloud for Uploading the videos into Youtube and Login using Google AND your email credentials for sending emails
### Recommended Setup

1. **Project dir**:
make sure you are in the project dir

2. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:  
   tswira.app uses environment variables to store sensitive data. You'll need to UPDATE a `.env` file at the root of the project with the CORRESPONADING variables
``
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''
AWS_S3_REGION_NAME = ''  
AWS_DEFAULT_ACL = ''

SECURE_KEY = ''

# FIRBASE CREDTENTIALS
FIREBASE_TYPE="service_account"
FIREBASE_PROJECT_ID=""
FIREBASE_PRIVATE_KEY_ID=""
FIREBASE_PRIVATE_KEY=""
FIREBASE_CLIENT_EMAIL=""
FIREBASE_CLIENT_ID=""
FIREBASE_AUTH_URI="https://accounts.google.com/o/oauth2/auth"
FIREBASE_TOKEN_URI="https://oauth2.googleapis.com/token"
FIREBASE_AUTH_PROVIDER_X509_CERT_URL="https://www.googleapis.com/oauth2/v1/certs"
FIREBASE_CLIENT_X509_CERT_URL=""
FIREBASE_UNIVERSE_DOMAIN="googleapis.com"


STRIPE_PUBLIC_KEY = ''
STRIPE_PRIVATE_KEY = ''
WEBHOOK_SECRET = ''
STRIPE_PUBLIC_TEST_KEY = ''
STRIPE_PRIVATE_TEST_KEY = ''
WEBHOOK_SECRET_TEST = ''

HF_TOKEN = ''

FRONT_END_URL = "http://localhost:5173/"
BACKEND_URL = 'http://localhost:8000/'
DEBUG = 1
DB_PATH = '.'
``







5. **Make and Apply migrations**:
    ```bash
    python manage.py makemigrations
    ```

    ```bash
    python manage.py migrate
    ```

6. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

The server should now be running on `http://127.0.0.1:8000`.

## Core Components

- **Django Rest Framework (DRF)**: We use DRF to build the API that serves the frontend and external integrations.
- **AWS S3**: File storage for the generated videos and images.
- **Django Q**: Task scheduling system that handles periodic operations.
  
## Local vs Production

For local development, SQLite is used as the database for simplicity. In production, Reelze.app runs oN SQLITE with an ONRENDER.COM hosting the Django app.

### Production Setup

In production, ensure to:
- Set `DEBUG=False` in the `.env` file.
- Set up a proper storage backend for media files (AWS S3).
- Use `gunicorn` or `uwsgi` to serve the application or in ONRENDER use `python manage.py runserver & python manage.py start_qcluster`
  
## Troubleshooting

- **Database errors**: Ensure migrations are applied (`python manage.py migrate`) and the correct database URL is configured.
- **AWS S3 issues**: Make sure the AWS credentials are correctly set in the environment variables and that the permissions allow read/write access to the bucket.

