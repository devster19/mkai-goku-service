FROM public.ecr.aws/lambda/python:3.11

# Copy function code
COPY app/ app/
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt --target "/var/task"

# Set the CMD to your handler (function name in app.main)
CMD ["app.main.lambda_handler"]
