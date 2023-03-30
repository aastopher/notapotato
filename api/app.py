from fastapi import FastAPI, Response
from pydantic import BaseModel
import subprocess

# Create the FastAPI instance
app = FastAPI()

# Define the response model for your API endpoint
class PotatoImage(BaseModel):
    image: bytes
    content_type: str

# Define the endpoint to generate the image
@app.get("/potato", response_model=PotatoImage)
async def generate_potato():
    # Run the script to generate the image and capture the output
    output = subprocess.check_output(["python", "gen_potato.py"])

    # Return the image as a bytes object with content type "image/png"
    return PotatoImage(image=output, content_type="image/png")
