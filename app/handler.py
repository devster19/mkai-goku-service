from app.main import app
from mangum import Mangum

# Create the ASGI handler
asgi_handler = Mangum(app)

def handler(event, context):
    """AWS Lambda handler function"""
    return asgi_handler(event, context)
