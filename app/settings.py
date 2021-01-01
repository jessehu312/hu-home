"""Settings configuration - Configuration for environment variables can go in here."""

import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv('FLASK_ENV', default='production')
DEBUG = ENV == 'development'
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{pathlib.Path().absolute()}/temp.db')
SECRET_KEY = os.getenv('SECRET_KEY', default='octocat')
SQLALCHEMY_TRACK_MODIFICATIONS = False

FIREBASE_ADMIN_CONFIG = {
  'project_id': os.getenv('PROJECT_ID'),
  'private_key': os.getenv('PRIVATE_KEY'),
  'client_email': os.getenv('CLIENT_EMAIL'),
  'type':  os.getenv('TYPE'),
  'private_key_id': os.getenv('PRIVATE_KEY_ID'),
  'client_id': os.getenv('CLIENT_ID'),
  'auth_uri': os.getenv('AUTH_URI'),
  'token_uri': os.getenv('TOKEN_URI'),
  'auth_provider_x509_cert_url': os.getenv('AUTH_PROVIDER_X590_CERT_URL'),
  'client_x509_cert_url': os.getenv('CLIENT_X509_CERT_URL'),
}

FIREBASE_CLIENT_CONFIG = {
  'apiKey': os.getenv('API_KEY'),
  'authDomain': os.getenv('AUTH_DOMAIN'),
  'projectId': os.getenv('PROJECT_ID'),
  'storageBucket': os.getenv('STORAGE_BUCKET'),
  'messagingSenderId': os.getenv('MESSAGING_SENDER_ID'),
  'appId': os.getenv('APP_ID'),
  'measurementId': os.getenv('MEASUREMENT_ID')
}

RADAR_PUBLISHABLE_KEY = os.getenv('RADAR_PUBLISHABLE_KEY')