import os
from fastapi import FastAPI
import uvicorn
from openai import OpenAI
import openai
from models import TextRequest,ImageRequest
from fastapi.responses import FileResponse
import base64
import dotenv
import uuid

import traceback
from logging import getLogger

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello image gen"}



client = OpenAI(
    # This is the default and can be omitted
    api_key = os.getenv("OPEN_API_KEY")
)


@app.post("/generate-text")
async def generate_text(req: TextRequest):
    try:
        stream = client.responses.create(
            model="gpt-4o",
            instructions="You are a coding assistant that talks like a pirate.",
            input=req.prompt,
            stream=False,
        )

        return(stream.output[0].content[0].text)

    except Exception as e:
        return {"error": str(e)}



@app.post("/generate-image")
async def generate_image(req: ImageRequest):
    try:
        response = client.responses.create(
            model="gpt-4o",
            instructions="You only generate anime style pictures",
            input=req.prompt,
            tools=[{"type": "image_generation"}],
        )

        image_data = [
            output.result
            for output in response.output
            if output.type == "image_generation_call"
        ]

        if image_data:
            image_base64 = image_data[0]
            image_id = str(uuid.uuid4()) + ".png"
            image_path = os.path.join(IMAGE_DIR, image_id)

            with open(image_path, "wb") as f:
                f.write(base64.b64decode(image_base64))

            return FileResponse(image_path, media_type="image/png")
        else:
            return {"error": "No image data returned."}

    except Exception as e:
        return {"error": str(e)}


from utils import find_free_port

if __name__ == "__main__":
    """
    Run the main only for debugging purpose, as it is assigning a
    random (free) port to run the API.

    In a production set-up please run the API in its container
    or call uvicorn directly from the CLI:
    uvicorn src.app:app --host 0.0.0.0 --port {DESIRED PORT}
    """
    logger = getLogger(__name__)
    port = find_free_port()
    logger.info(f"Running API on port: {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)