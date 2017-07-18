import os

PROJECT_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__name__), '..')) + '/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_BUCKET = "diginehru"
# SERVER_BUCKET = os.environ['SERVER_BUCKET']
S3_BUCKET_URL = 'https://s3.ap-south-1.amazonaws.com/'
S3_BUCKET = S3_BUCKET_URL + SERVER_BUCKET + '/'
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
