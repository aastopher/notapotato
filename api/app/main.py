from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from pydantic import BaseModel
import subprocess
from loguru import logger

# Configure logger
logger.add(
    "logs/main.log",
    rotation="25 MB",
    retention="30 days",
    colorize=True,
    format="{time} | {level} | {name}:{function}:{line} - {message}",
    level="INFO",
)

app = FastAPI()

# Define Rate limiter and add exception handler
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Define the response model for the endpoint
class Image(BaseModel):
    """
    Image Object

    Attributes:
        image (bytes): base64 string representation of the image.
        content_type (str): The MIME type of the image.
    """

    image: bytes
    content_type: str


# Define the endpoint to generate the image
@app.get(
    "/potato",
    response_model=Image,
    summary="Generate Potato Image",
    description="Generates an image of a potato and returns it as a base64 string.",
)
@limiter.limit("100/minute")
async def generate_potato(request: Request):
    """
    Generates a potato image.

    This endpoint runs a script to generate a potato image, returning the image as a base64 string. The request is rate-limited to 100 requests per minute per client IP.

    Args:
        request (Request): The incoming request object, used for rate-limiting purposes.

    Returns:
        Image: A response containing the base64 image data and its content type.

    Raises:
        Exception: If there is an error while generating the potato image.
    """
    logger.info("Generating potato")
    try:
        # Run the script to generate the image and capture the output
        output = subprocess.check_output(["python", "gen_potato.py"])
        logger.info("Potato generated successfully!")
    except Exception as e:
        logger.info(f"Generating potato failed: {e}")
        raise e

    # Return the image as a bytes object with content type "image/png"
    return Image(image=output, content_type="image/png")
