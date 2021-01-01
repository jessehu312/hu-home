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

FIREBASE_CLIENT_CONFIG={
  'apiKey': os.getenv('API_KEY'),
  'authDomain': os.getenv('AUTH_DOMAIN'),
  'projectId': os.getenv('PROJECT_ID'),
  'storageBucket': os.getenv('STORAGE_BUCKET'),
  'messagingSenderId': os.getenv('MESSAGING_SENDER_ID'),
  'appId': os.getenv('APP_ID'),
  'measurementId': os.getenv('MEASUREMENT_ID')
}
FIREBASE_ADMIN_CONFIG={
  'privateKey': os.getenv('PRIVATE_KEY'),
  'clientEmail': os.getenv('CLIENT_EMAIL'),
  'projectId': os.getenv('PROJECT_ID')
}