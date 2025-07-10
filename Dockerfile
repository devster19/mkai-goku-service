FROM public.ecr.aws/lambda/python:3.11

WORKDIR /var/task

# Install system dependencies if needed (uncomment if you need build tools)
# RUN yum install -y gcc

# Copy function code
COPY app/ app/
COPY requirements.txt ./
COPY start.sh ./

# Install dependencies to /var/task
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose port for local dev
EXPOSE 8000

# For local dev: run start.sh (uncomment below for local Docker run)
ENTRYPOINT ["/bin/bash", "./start.sh"]

# For AWS Lambda: set the CMD to your handler (function name in app.lambda_handler)
# CMD ["app.lambda_handler.lambda_handler"]
