import os
import re
import uuid
from datetime import datetime

from django.conf import settings


def format_time(time_str):
    try:
        dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S,%f')
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return time_str


def read_log_file(file_path, lines=100, trace_id=None, level=''):
    try:
        with open(file_path, 'r') as file:
            log_lines = file.readlines()
    except FileNotFoundError:
        return []

    # Reverse the log lines for descending order
    log_lines.reverse()

    # Filter by trace ID if provided
    if trace_id:
        log_lines = [line for line in log_lines if trace_id in line]

    # Filter by log level if provided
    if level and level.upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        log_lines = [line for line in log_lines if f'{level}' in line]

    # Format the timestamps in the logs
    formatted_log_lines = []
    for line in log_lines:
        match = re.match(r'(\w+\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d+)\s+(.*)', line)
        if match:
            timestamp, rest = match.groups()
            formatted_log_lines.append(f"{format_time(timestamp)} {rest}")
        else:
            formatted_log_lines.append(line)

    return formatted_log_lines[:lines]


def save_picture_to_folder(uploaded_file, folder_name: str):
    # Define the folder path where you want to save the pictures
    folder_path: str = os.path.join(settings.MEDIA_ROOT, folder_name)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Generate a unique file name for the picture
    file_name: str = uploaded_file.name
    file_name: str = file_name.replace(' ', '_')
    extension: str = file_name.split('.')[-1]

    # Replace the file name with a unique name
    timestamp: str = datetime.now().strftime('%Y%m%d_%H%M%S')
    final_file_name: str = f"{file_name.split('.')[0]}_{uuid.uuid4()}_{timestamp}.{extension}"

    # Limit the file name to 100 characters
    if len(final_file_name) > 100:
        final_file_name = final_file_name[-100:]

    # Join the folder path and the file name
    file_path: str = os.path.join(folder_path, final_file_name)

    # Open the file in write binary mode and write the picture data
    with open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    server_url = settings.SERVER_URL
    file_url = f"{server_url}{file_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL).replace('//', '/')}"

    # Return the file path
    return file_url
