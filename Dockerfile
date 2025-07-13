# Use the official AWS Lambda Python runtime as base image for ARM64
FROM public.ecr.aws/lambda/python:3.11-arm64

# Copy requirements file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using pip
RUN pip install -r requirements.txt

# Copy function code
COPY app/ ${LAMBDA_TASK_ROOT}/app/

# Set the CMD to your handler
CMD ["app.handler.handler"]
