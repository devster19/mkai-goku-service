FROM public.ecr.aws/lambda/python:3.11

# Copy requirements first for better Docker cache
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY app/ ${LAMBDA_TASK_ROOT}/app/

# Set the CMD to your handler
CMD ["app.lambda_handler.lambda_handler"]
