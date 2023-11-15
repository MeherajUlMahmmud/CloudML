import os

SECRET_KEY = '38dd56f56d405e02ec0ba4be4607eaab'
UPLOAD_FOLDER = "static/uploads/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Database
MONGO_URI = 'mongodb+srv://meheraj:ocQYjfJyctV0rRBY@cluster0.3mqtt.mongodb.net/cloudml?retryWrites=true&w=majority'

# JWT
JWT_SECRET_KEY = SECRET_KEY

# Cron Job
CRON_JOB_TIMEZONE = 'Asia/Dhaka'
CRON_JOB_ENABLED = True

# Celery Configuration Options
CELERY_TIMEZONE = 'Asia/Dhaka'  # change to your local timezone
CELERY_TASK_TRACK_STARTED = True  # track started tasks state
CELERY_TASK_TIME_LIMIT = 30 * 60  # time limit in seconds
CELERY_TASK_SOFT_TIME_LIMIT = 30 * 60  # soft time limit in seconds
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
