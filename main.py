import os
import base64
import uuid

from logging import getLogger

import uvicorn
from config import client, client_google,client_anth,client_groq
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from models import TextRequest, ImageRequest,Aimodel
from typing import Annotated

from google.genai import types
from google import genai
from PIL import Image
from io import BytesIO

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello image gen"}


@app.post("/generate-text")
async def generate_text(model: Aimodel, req: TextRequest):
    if model == "openai":
        try:
            stream = client.responses.create(
                model="gpt-4o",
                instructions="You are a coding assistant that talks like a pirate.",
                input=req.prompt,
                stream=False,
            )

            return stream.output[0].content[0].text

        except Exception as e:
            return {"error": str(e)}
    elif model == "gemini":
        response = client_google.models.generate_content(
        model="gemini-2.5-flash", contents=req.prompt
        )
        return(response.text)
    elif model == "Groq":
        chat_completion = client_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": req.prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return(chat_completion.choices[0].message.content)
    else:
        return ("WTF")


@app.post("/generate-image")
async def generate_image(model: Aimodel, req: ImageRequest):
    if model == "openai":
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
    elif model == "gemini":
        response = client_google.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=req.prompt,
            config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
            )
        )

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                image = Image.open(BytesIO((part.inline_data.data)))
                image.save('gemini-native-image.png')
                return FileResponse("gemini-native-image.png", media_type="image/png")



@app.post("/picture_analysis/")
async def create_file(file: Annotated[UploadFile, File()], input):
    # Read the image bytes
    image_bytes = await file.read()

    response = client_google.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
      types.Part.from_bytes(
        data=image_bytes,
        mime_type='image/jpeg',
      ),
      input
    ]
  )
    return {"caption": response.text}


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
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True, ssl_certfile="./code-server.tailb8fd1f.ts.net.crt", ssl_keyfile="./code-server.tailb8fd1f.ts.net.key")
