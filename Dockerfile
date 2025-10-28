# Use AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Copy function code
COPY process_profile.py ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler
CMD [ "process_profile.lambda_handler" ]
