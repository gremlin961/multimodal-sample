import json
from fastapi import FastAPI, File, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import base64
from pkg.SecurePrompt import GetValue
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part


# Function to generate text using a Vertex AI generative model
def generate_text(project_id: str, location: str, b64_image: str, prompt: str, mimeType: str) -> str:
    # Initialize Vertex AI client
    vertexai.init(project=project_id, location=location)

    # Create a GenerativeModel object for the specified model
    multimodal_model = GenerativeModel("gemini-pro-vision")

    # Generate content using the model, passing the image and prompt
    response = multimodal_model.generate_content(
        [
            Part.from_data(
                data=base64.b64decode(b64_image), mime_type=mimeType # Use the mime_type variable
            ),
            Part.from_text(prompt),  # Encapsulate the prompt in a Part object
        ]
    )

    # Return the generated text
    return response.text

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.post("/")
async def upload_image(image: bytes = File(...), project_id: str = Form(...), secret_name: str = Form(...), media_type: str = Form("image")):  # Add media_type parameter
    try:
        # Get variables from form
        PROJECT_ID = project_id
        SECRET_ID = secret_name
        LOCATION = "us-central1"  # Set the location of your Vertex AI model
        SECRET_ALIAS = "prod"

        # Get parameters from Secret Manager
        secret_value = GetValue(PROJECT_ID, SECRET_ID, SECRET_ALIAS)

        # Extract the "text" attribute from the secret_value
        secret_value_json = json.loads(secret_value)
        prompt_text = secret_value_json["prompt"]["parts"][0]["text"]

        # Encode image
        encoded_image = base64.b64encode(image).decode('utf-8')

        # Set mime type based on media type selection
        mimeType = "image/jpeg" if media_type == "image" else "video/mp4"

        # Generate text using Vertex AI, passing the mime type argument
        generated_text = generate_text(PROJECT_ID, LOCATION, encoded_image, prompt_text, mimeType)

        # Return results including generated_text
        return {"encoded_image": encoded_image, "project_id": project_id, "secret_name": secret_name, "prompt_text": prompt_text, "generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))