FROM public.ecr.aws/lambda/python:3.11

# Install system dependencies if needed (uncomment if you need build tools)
# RUN yum install -y gcc

# Copy function code
COPY app/ app/
COPY requirements.txt ./

# Install dependencies to /var/task
RUN pip install --upgrade pip \
    && pip install -r requirements.txt --target /var/task

# (Optional) Show installed packages for debug
# RUN pip freeze

# Set the CMD to your handler (function name in app.main)
CMD ["app.main.lambda_handler"]
