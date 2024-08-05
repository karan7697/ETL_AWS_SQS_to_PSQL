content = """

# Fetch Rewards Data Engineering Take Home

# ETL_AWS_SQS_to_PSQL
Extracting data from AWS SQS queue, transforming the data by masking the PI information and loading the data to PSQL database using AWS CLI

## Overview

This project involves reading JSON data from an AWS SQS Queue, masking PII data (device_id and ip), and writing the transformed data to a PostgreSQL database. The setup uses Docker to run Postgres and Localstack locally, ensuring that you do not need an actual AWS account to complete this exercise.

## Prerequisites

- Docker
- Docker Compose
- `awscli-local`
- PostgreSQL client
- Python 3.x

## Installation and Setup

### 1. Clone the Repository

\`\`\`bash
git clone <repository-url>
cd <repository-directory>
\`\`\`

### 2. Start Docker Services

Ensure Docker and Docker Compose are installed. Then, start the required services:

\`\`\`bash
docker-compose up
\`\`\`

### 3. Verify Postgres Table Creation

Ensure the `user_logins` table is created in the PostgreSQL database:

1. Open a terminal or Command Prompt.
2. Connect to the PostgreSQL database using `psql`:

   \`\`\`bash
   psql -d postgres -U postgres -p 5432 -h localhost -W
   \`\`\`

   When prompted for a password, enter `postgres`.

3. List tables to verify:

   \`\`\`sql
   \dt
   \`\`\`

   You should see the `user_logins` table.

### 4. Check Messages in the SQS Queue

Verify that there are messages in the SQS queue:

\`\`\`bash
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
\`\`\`

### 5. Run the Python Script

Ensure Python and required packages are installed:

\`\`\`bash
pip install boto3 psycopg2-binary
\`\`\`

Run the ETL script:

\`\`\`bash
python etl.py
\`\`\`

### 6. Verify Data Insertion

Connect to the PostgreSQL database to verify the data insertion:

1. Open a terminal or Command Prompt.
2. Connect to the PostgreSQL database using `psql`:

   \`\`\`bash
   psql -d postgres -U postgres -p 5432 -h localhost -W
   \`\`\`

3. Query the `user_logins` table:

   \`\`\`sql
   SELECT * FROM user_logins;
   \`\`\`

   You should see the data inserted from the SQS messages.

## Thought Process

### How will you read messages from the queue?

- Used `boto3` to interact with the SQS queue.
- Read messages in batches to handle multiple messages efficiently.

### What type of data structures should be used?

- Utilized Python dictionaries to parse JSON messages and store the transformed data.

### How will you mask the PII data so that duplicate values can be identified?

- Used SHA-256 hashing to mask `device_id` and `ip`.
- Ensured the same input generates the same masked output to identify duplicates.

### What will be your strategy for connecting and writing to Postgres?

- Used `psycopg2` to connect and write to the PostgreSQL database.
- Inserted records after transforming and masking the required fields.

### Where and how will your application run?

- The application runs locally using Docker for PostgreSQL and Localstack.
- The Python script processes the messages, transforms the data, and writes it to the database.

## Questions and Answers

### How would you deploy this application in production?

1. **Containerization**: Use Docker to containerize the application for consistent deployment across environments.
2. **Orchestration**: Use Kubernetes or ECS for orchestration to manage container scaling, rolling updates, and health monitoring.
3. **CI/CD Pipeline**: Implement a CI/CD pipeline using tools like Jenkins, GitLab CI, or GitHub Actions to automate testing and deployment.
4. **Environment Variables**: Use environment variables to manage configuration settings like database credentials, AWS credentials, and other sensitive information.
5. **Logging and Monitoring**: Integrate logging (using tools like ELK stack) and monitoring (using tools like Prometheus and Grafana) for observability.

### What other components would you want to add to make this production ready?

1. **Error Handling**: Implement robust error handling to catch and log exceptions.
2. **Data Validation**: Add data validation to ensure data integrity and consistency.
3. **Security**: Encrypt sensitive data and use secure methods to handle credentials.
4. **Scalability**: Design for scalability to handle increasing volumes of data.
5. **Unit Tests**: Add unit tests to validate functionality and prevent regressions.

### How can this application scale with a growing dataset?

1. **Horizontal Scaling**: Use container orchestration to horizontally scale SQS consumers and database instances based on load.
2. **Batch Processing**: Process messages in batches to improve efficiency.
3. **Database Sharding**: Implement database sharding to distribute data across multiple instances.
4. **Message Queue Tuning**: Tune SQS settings for optimal performance, such as increasing the message visibility timeout and batch size.

### How can PII be recovered later on?

1. **Secure Storage**: Store original PII data in a secure, encrypted database.
2. **Key Management**: Use a key management service (e.g., AWS KMS) to manage encryption keys.
3. **Access Control**: Implement strict access controls to ensure only authorized personnel can decrypt and access PII data.
4. **Audit Logging**: Maintain audit logs to track access and modifications to PII data.

### What are the assumptions you made?

1. The input JSON structure is consistent across messages.
2. Masking PII data does not require the ability to reverse the masking.
3. The application runs in a controlled, secure environment.
4. The default `create_date` value is acceptable for messages missing this field.

## Next Steps

1. **Implement unit tests**: Validate functionality.
2. **Optimize ETL process**: Improve performance.
3. **Enhance monitoring and alerting**: For production environments.
4. **Improve data validation and error handling**: Continuously enhance.