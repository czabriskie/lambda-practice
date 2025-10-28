```markdown
# Lambda Function Demo

A simple AWS Lambda function that processes multiple input values and performs calculations.

## Prerequisites

- Docker installed on your machine
- Python 3.11+ (for local development)
- AWS CLI configured (for deployed testing)

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

## Testing via Custom Domain (Recommended)

The easiest way to test the API is using the custom domain:

### Basic API Test

```bash
curl -X POST https://api.follicle-force-3000.com/process-profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "interests": ["coding", "music", "travel"]
  }'
```

**Expected Response:**
```json
{
  "message": "Profile processed successfully",
  "original_input": {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "interests": ["coding", "music", "travel"]
  },
  "processed_profile": {
    "full_name": "John Doe",
    "email_domain": "example.com",
    "age_group": "adult",
    "interest_count": 3,
    "profile_score": 100,
    "created_at": "2025-10-28T12:33:25.695544"
  }
}
```

### Test Different Scenarios

**Valid adult user:**
```bash
curl -X POST https://api.follicle-force-3000.com/process-profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@company.com",
    "age": 25,
    "interests": ["reading", "hiking", "photography"]
  }'
```

**Minor user:**
```bash
curl -X POST https://api.follicle-force-3000.com/process-profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Charlie Brown",
    "email": "charlie@school.edu",
    "age": 16,
    "interests": ["gaming", "music"]
  }'
```

**Senior user:**
```bash
curl -X POST https://api.follicle-force-3000.com/process-profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Robert Wilson",
    "email": "bob@retirement.com",
    "age": 70,
    "interests": ["gardening", "reading"]
  }'
```

**Invalid email test:**
```bash
curl -X POST https://api.follicle-force-3000.com/process-profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bob Smith",
    "email": "invalid-email",
    "age": 45,
    "interests": ["sports"]
  }'
```

**Empty interests:**
```bash
curl -X POST https://api.follicle-force-3000.com/process-profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "age": 35,
    "interests": []
  }'
```

**Minimal data:**
```bash
curl -X POST https://api.follicle-force-3000.com/process-profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "",
    "email": "",
    "age": 0,
    "interests": []
  }'
```

## Testing via API Gateway (Alternative)

You can also test using the direct API Gateway URL:

### Basic API Gateway Test

```bash
curl -X POST https://3curjopzvj.execute-api.us-west-2.amazonaws.com/process-profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "interests": ["coding", "music", "travel"]
  }'
```

## Testing Deployed Lambda Function (Direct)

Once your function is deployed to AWS, you can also test it directly using the AWS CLI:

### Prerequisites for Deployed Testing
- AWS CLI installed and configured
- Appropriate IAM permissions to invoke Lambda functions
- Function deployed with name `profileScorer` (or update the function name below)

### 1. Direct Lambda Invocation

```bash
aws lambda invoke \
  --function-name profileScorer \
  --payload $(echo '{"body": "{\"name\":\"John Doe\",\"email\":\"john@example.com\",\"age\":30,\"interests\":[\"coding\",\"music\"]}"}' | base64) \
  response.json
```

### 2. Alternative: Using a Payload File

Create a file `test-payload.json`:
```json
{
  "body": "{\"name\":\"John Doe\",\"email\":\"john@example.com\",\"age\":30,\"interests\":[\"coding\",\"music\"]}"
}
```

Then invoke:
```bash
aws lambda invoke \
  --function-name profileScorer \
  --payload fileb://test-payload.json \
  response.json
```

### 3. Check the Response

View the response:
```bash
cat response.json
```

### 4. Region Configuration

If your function is in a specific region, specify it:
```bash
aws lambda invoke \
  --region us-west-2 \
  --function-name profileScorer \
  --payload fileb://test-payload.json \
  response.json
```

Or set the default region:
```bash
export AWS_DEFAULT_REGION=us-west-2
```

## Understanding the Response

The API returns a JSON object with three main sections:

- **message**: Status message indicating success or failure
- **original_input**: The exact data you sent to the API
- **processed_profile**: The calculated results including:
  - `full_name`: Properly capitalized name
  - `email_domain`: Domain extracted from email address
  - `age_group`: "minor" (< 18), "adult" (18-64), or "senior" (65+)
  - `interest_count`: Number of interests provided
  - `profile_score`: Score out of 100 based on data completeness
  - `created_at`: Timestamp when the profile was processed

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
- **ResourceNotFoundException**: Check that the function name and region are correct
- **Invalid base64 error**: Use `fileb://` prefix for payload files or ensure proper base64 encoding
- **API Gateway 404**: Verify the endpoint URL and path are correct
- **CORS issues**: If testing from a browser, ensure CORS is configured on the API Gateway
- **Domain not resolving**: Ensure DNS is properly configured for the custom domain

## Deployment

To deploy to AWS Lambda:
1. Push the image to Amazon ECR
2. Create a Lambda function using the container image
3. Configure triggers (API Gateway, etc.)
4. Set up custom domain mapping (optional)
` ` `

The key additions are:
1. **Custom Domain section** at the top (marked as "Recommended")
2. **Sample response** showing the actual JSON structure
3. **Understanding the Response** section explaining what each field means
4. **Additional test scenarios** including edge cases
5. **Domain troubleshooting** in the troubleshooting section