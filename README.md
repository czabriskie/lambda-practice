# Lambda Function Demo

A simple AWS Lambda function that processes multiple input values and performs calculations.

## Prerequisites

- Docker installed on your machine
- Python 3.11+ (for local development)

## Project Structure

```
.
├── Dockerfile
├── lambda_function.py
├── requirements.txt (optional)
└── README.md
```

## Local Development

### 1. Build the Docker Image

```bash
docker build -t my-lambda-function .
```

### 2. Run the Container Locally

```bash
docker run -p 9000:8080 my-lambda-function
```

This starts the Lambda Runtime Interface Emulator on port 9000.

### 3. Test the Function

Open a new terminal and test with curl:

**User Profile Example:**
```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{"body": "{\"name\": \"john doe\", \"email\": \"john@example.com\", \"age\": 28, \"interests\": [\"coding\", \"music\"]}"}'

curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{"body": "{\"name\": \"jane smith\", \"email\": \"\", \"age\": 16, \"interests\": [\"gaming\"]}"}'
```

## Expected Response

You should see a JSON response like:

```json
{
  "statusCode": 200,
  "body": "{\"input\": {...}, \"result\": ...}"
}
```

## Stopping the Container

Press `Ctrl+C` in the terminal where the container is running, or:

```bash
docker ps
docker stop <container_id>
```

## Rebuilding After Changes

If you modify the code:

1. Stop the running container
2. Rebuild the image: `docker build -t my-lambda-function .`
3. Run again: `docker run -p 9000:8080 my-lambda-function`

## Troubleshooting

- **Port already in use**: Change the port mapping: `docker run -p 9001:8080 my-lambda-function`
- **Function not found**: Ensure your Python file is named `lambda_function.py` and contains `lambda_handler`
- **JSON parsing errors**: Make sure to properly escape quotes in your test JSON

## Deployment

To deploy to AWS Lambda:
1. Push the image to Amazon ECR
2. Create a Lambda function using the container image
3. Configure triggers (API Gateway, etc.)