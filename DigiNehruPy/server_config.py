import os
from settings import BASE_DIR
SERVER_BUCKET = "diginehru"
PROJECT_PATH = os.path.abspath(os.path.join(BASE_DIR, '..')) + '/'
# SERVER_BUCKET = os.environ['SERVER_BUCKET']
S3_BUCKET_URL = 'https://s3.ap-south-1.amazonaws.com/'
S3_BUCKET = S3_BUCKET_URL + SERVER_BUCKET + '/'
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
