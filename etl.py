import boto3
import hashlib
import json
import psycopg2
from datetime import datetime

# Constants
QUEUE_URL = "http://localhost:4566/000000000000/login-queue"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
REGION_NAME = "us-east-1"  # Specify a region

# Masking Function
def mask_pii(value):
    return hashlib.sha256(value.encode()).hexdigest()

# Read messages from SQS queue
def read_sqs_messages():
    sqs = boto3.client(
        'sqs',
        endpoint_url='http://localhost:4566',
        region_name=REGION_NAME,
        aws_access_key_id='dummy_access_key',  # Provide dummy access key
        aws_secret_access_key='dummy_secret_key'  # Provide dummy secret key
    )
    response = sqs.receive_message(QueueUrl=QUEUE_URL, MaxNumberOfMessages=10)
    messages = response.get('Messages', [])
    print(f"Received {len(messages)} messages")
    return messages

# Write data to Postgres
def write_to_postgres(records):
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cursor = conn.cursor()

    for record in records:
        print(f"Inserting record: {record}")
        cursor.execute(
            """
            INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                record['user_id'],
                record['device_type'],
                record['masked_ip'],
                record['masked_device_id'],
                record['locale'],
                record['app_version'],
                record['create_date'],
            ),
        )

    conn.commit()
    cursor.close()
    conn.close()

# Main function to perform ETL
def main():
    messages = read_sqs_messages()
    records = []

    for message in messages:
        body = json.loads(message['Body'])
        user_id = body['user_id']
        device_type = body['device_type']
        masked_ip = mask_pii(body['ip'])
        masked_device_id = mask_pii(body['device_id'])
        locale = body['locale']
        app_version = int(body['app_version'].split('.')[0])
        
        # Handle missing 'create_date' key
        create_date_str = body.get('create_date', '2000-01-01T00:00:00Z')
        create_date = datetime.strptime(create_date_str, "%Y-%m-%dT%H:%M:%SZ").date()

        record = {
            'user_id': user_id,
            'device_type': device_type,
            'masked_ip': masked_ip,
            'masked_device_id': masked_device_id,
            'locale': locale,
            'app_version': app_version,
            'create_date': create_date,
        }
        records.append(record)
    
    if records:
        write_to_postgres(records)
    else:
        print("No records to insert")

if __name__ == "__main__":
    main()
